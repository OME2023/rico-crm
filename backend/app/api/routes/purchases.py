from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP

from app.db.session import get_db
from app.models.purchases import PurchaseOrder, PurchaseOrderItem
from app.models.core import Product, Supplier
from app.models.stock import Stock
from app.models.audit import AuditLog
from app.schemas.purchases import PurchaseCreateIn, PurchaseAddItemIn, PurchaseOut, PurchaseItemOut

router = APIRouter(prefix="/purchases", tags=["purchases"])

def dec(v) -> Decimal:
    return Decimal(str(v))

def money(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

@router.post("", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
def create_po(payload: PurchaseCreateIn, db: Session = Depends(get_db)):
    if not db.get(Supplier, payload.supplier_id):
        raise HTTPException(400, "Proveedor inexistente")
    po = PurchaseOrder(supplier_id=payload.supplier_id, status="open")
    db.add(po); db.commit(); db.refresh(po)
    return po

@router.post("/{po_id}/add", response_model=PurchaseItemOut)
def add_item(po_id: int, payload: PurchaseAddItemIn, db: Session = Depends(get_db)):
    po = db.get(PurchaseOrder, po_id)
    if not po or po.status != "open":
        raise HTTPException(400, "OC inválida")
    if not db.get(Product, payload.product_id):
        raise HTTPException(400, "Producto inexistente")

    it = PurchaseOrderItem(
        order_id=po_id,
        product_id=payload.product_id,
        warehouse_id=payload.warehouse_id,
        qty_base=payload.qty_base,
        cost_net=payload.cost_net,
        vat_rate=payload.vat_rate if payload.vat_rate in (21,19) else 21,
    )
    db.add(it); db.commit(); db.refresh(it)
    return it

@router.post("/{po_id}/receive", response_model=dict)
def receive(po_id: int, db: Session = Depends(get_db)):
    po = db.get(PurchaseOrder, po_id)
    if not po or po.status != "open":
        raise HTTPException(400, "OC no abierta")

    items = db.query(PurchaseOrderItem).filter_by(order_id=po_id).all()
    if not items:
        raise HTTPException(400, "OC sin ítems")

    for it in items:
        # 1) Costo promedio ponderado con cantidad PREVIA (antes de sumar stock)
        p = db.get(Product, it.product_id)

        prev_qty = db.query(func.coalesce(func.sum(Stock.qty_base), 0))\
                     .filter(Stock.product_id == it.product_id).scalar() or 0
        prev_qty = dec(prev_qty)                 # cantidad previa real
        prev_cost = dec(p.cost_net or 0)

        new_qty = prev_qty + dec(it.qty_base)
        if new_qty > 0:
            avg = (prev_qty * prev_cost + dec(it.qty_base) * dec(it.cost_net)) / new_qty
            before_cost = p.cost_net
            p.cost_net = money(avg)

            vat = it.vat_rate if it.vat_rate in (21,19) else 21
            p.cost_gross = money(dec(p.cost_net) * (dec(1) + dec(vat)/dec(100)))

            db.add(AuditLog(
                entity="product", entity_id=p.id,
                action="cost_avg_update",
                detail=f"before_net={before_cost}, after_net={p.cost_net}, qty_prev={prev_qty}, qty_rec={it.qty_base}, cost_rec={it.cost_net}"
            ))

        # 2) Aumentar stock (después de calcular el costo)
        st = db.query(Stock).filter_by(product_id=it.product_id, warehouse_id=it.warehouse_id).first()
        if not st:
            st = Stock(product_id=it.product_id, warehouse_id=it.warehouse_id, qty_base=dec(0))
            db.add(st)
        before_qty = dec(st.qty_base or 0)
        st.qty_base = before_qty + dec(it.qty_base)

        db.add(AuditLog(
            entity="stock", entity_id=it.product_id,
            action="stock_increase",
            detail=f"prod {it.product_id}, wh {it.warehouse_id}, +{it.qty_base}"
        ))

    po.status = "received"
    db.commit()
    return {"ok": True}
