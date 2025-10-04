from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP

from app.db.session import get_db
from app.models.sales import SalesOrder, SalesOrderItem
from app.models.core import Product
from app.models.stock import Stock
from app.models.customers import Customer
from app.schemas.orders import OrderCreateIn, OrderAddItemIn, OrderOut, OrderItemOut, OrderSummaryOut

router = APIRouter(prefix="/orders", tags=["orders"])

def dec(val: float | int | str) -> Decimal:
    return Decimal(str(val))

def money(x: Decimal) -> float:
    return float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreateIn, db: Session = Depends(get_db)):
    if not db.get(Customer, payload.customer_id):
        raise HTTPException(400, "Cliente inexistente")
    o = SalesOrder(customer_id=payload.customer_id, discount_pct=payload.discount_pct or 0, status="cart")
    db.add(o); db.commit(); db.refresh(o)
    return o

@router.post("/{order_id}/add", response_model=dict)
def add_item(order_id: int, payload: OrderAddItemIn, db: Session = Depends(get_db)):
    o = db.get(SalesOrder, order_id)
    if not o or o.status != "cart":
        raise HTTPException(400, "Pedido inválido")
    p = db.get(Product, payload.product_id)
    if not p:
        raise HTTPException(400, "Producto inexistente")

    item = SalesOrderItem(
        order_id=order_id,
        product_id=payload.product_id,
        warehouse_id=payload.warehouse_id,
        qty_base=payload.qty_base,         # Decimal
        price_net=payload.price_net,       # Decimal unitario
        vat_rate=int(p.vat_override or 21)
    )
    db.add(item); db.commit(); db.refresh(item)
    return {"ok": True, "item_id": item.id}

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = db.get(SalesOrder, order_id)
    if not o:
        raise HTTPException(404, "Pedido no encontrado")
    return o

@router.get("/{order_id}/items", response_model=list[OrderItemOut])
def get_items(order_id: int, db: Session = Depends(get_db)):
    return db.query(SalesOrderItem).filter_by(order_id=order_id).all()

@router.get("/{order_id}/summary", response_model=OrderSummaryOut)
def summary(order_id: int, db: Session = Depends(get_db)):
    o = db.get(SalesOrder, order_id)
    if not o: raise HTTPException(404, "Pedido no encontrado")

    items = db.query(SalesOrderItem).filter_by(order_id=order_id).all()
    subtotal_net = sum((dec(i.price_net) * dec(i.qty_base) for i in items), start=Decimal("0"))
    discount_pct = dec(o.discount_pct or 0) / dec(100)
    subtotal_disc = subtotal_net * (dec(1) - discount_pct)

    vat_21 = sum((dec(i.price_net) * dec(i.qty_base) * dec("0.21") for i in items if i.vat_rate == 21), start=Decimal("0"))
    vat_19 = sum((dec(i.price_net) * dec(i.qty_base) * dec("0.19") for i in items if i.vat_rate == 19), start=Decimal("0"))

    # El descuento se aplica sobre el neto; el IVA se calcula sobre el precio neto sin descuento (alternativa: proporcional).
    total_gross = subtotal_disc + vat_21 + vat_19

    return OrderSummaryOut(
        id=o.id,
        subtotal_net=money(subtotal_net),
        discount_pct=float(o.discount_pct or 0),
        subtotal_net_after_discount=money(subtotal_disc),
        vat_21=money(vat_21),
        vat_19=money(vat_19),
        total_gross=money(total_gross),
    )

@router.post("/{order_id}/confirm", response_model=dict)
def confirm(order_id: int, db: Session = Depends(get_db)):
    o = db.get(SalesOrder, order_id)
    if not o: raise HTTPException(404, "Pedido no encontrado")
    if o.status != "cart":
        raise HTTPException(400, "Pedido no está en carrito")

    items = db.query(SalesOrderItem).filter_by(order_id=order_id).all()
    # Validar stock disponible por item/depósito
    for it in items:
        st = db.query(Stock).filter_by(product_id=it.product_id, warehouse_id=it.warehouse_id).first()
        available = st.qty_base if st else 0
        if dec(available) < dec(it.qty_base):
            raise HTTPException(400, f"Stock insuficiente para producto {it.product_id} en depósito {it.warehouse_id}")

    # Descontar stock
    for it in items:
        st = db.query(Stock).filter_by(product_id=it.product_id, warehouse_id=it.warehouse_id).first()
        st.qty_base = dec(st.qty_base or 0) - dec(it.qty_base)

    o.status = "confirmed"
    db.commit()
    return {"ok": True}
