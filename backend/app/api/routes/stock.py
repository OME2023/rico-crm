from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from app.db.session import get_db
from app.models.stock import Stock, StockMin, Warehouse
from app.models.core import Product
from app.schemas.stock import StockAdjustIn, StockMinSetIn, StockRowOut, StockAlertOut

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("", response_model=list[StockRowOut])
def consolidated(db: Session = Depends(get_db)):
    rows = (db.query(Stock.product_id, func.sum(Stock.qty_base).label("qty"))
              .group_by(Stock.product_id).all())
    return [{"product_id": r.product_id, "qty_base": float(r.qty or 0)} for r in rows]

@router.post("/adjust")
def adjust(payload: StockAdjustIn, db: Session = Depends(get_db)):
    # Validaciones básicas
    if not db.get(Product, payload.product_id):
        raise HTTPException(400, "Producto inexistente")
    if not db.get(Warehouse, payload.warehouse_id):
        raise HTTPException(400, "Depósito inexistente")

    row = db.query(Stock).filter_by(product_id=payload.product_id,
                                    warehouse_id=payload.warehouse_id).first()
    if not row:
        row = Stock(product_id=payload.product_id,
                    warehouse_id=payload.warehouse_id,
                    qty_base=Decimal("0"))
        db.add(row)

    current = row.qty_base if row.qty_base is not None else Decimal("0")
    # payload.qty_delta ya es Decimal por condecimal()
    row.qty_base = current + payload.qty_delta
    db.commit(); db.refresh(row)
    return {"ok": True, "qty_base": float(row.qty_base or 0)}

@router.post("/min")
def set_min(payload: StockMinSetIn, db: Session = Depends(get_db)):
    if not db.get(Product, payload.product_id):
        raise HTTPException(400, "Producto inexistente")
    if not db.get(Warehouse, payload.warehouse_id):
        raise HTTPException(400, "Depósito inexistente")
    row = db.query(StockMin).filter_by(product_id=payload.product_id,
                                       warehouse_id=payload.warehouse_id).first()
    if not row:
        row = StockMin(product_id=payload.product_id,
                       warehouse_id=payload.warehouse_id,
                       min_qty=payload.min_qty)  # Decimal
        db.add(row)
    else:
        row.min_qty = payload.min_qty  # Decimal
    db.commit(); db.refresh(row)
    return {"ok": True, "min_qty": float(row.min_qty or 0)}

@router.get("/alerts", response_model=list[StockAlertOut])
def alerts(db: Session = Depends(get_db)):
    agg = (db.query(Stock.product_id, Stock.warehouse_id,
                    func.coalesce(func.sum(Stock.qty_base), 0).label("qty"))
             .group_by(Stock.product_id, Stock.warehouse_id).subquery())

    out = []
    mins = db.query(StockMin).all()
    for m in mins:
        qty = db.query(agg.c.qty).filter(
            agg.c.product_id == m.product_id,
            agg.c.warehouse_id == m.warehouse_id
        ).scalar() or 0
        if float(qty) < float(m.min_qty or 0):
            out.append({
                "product_id": m.product_id,
                "warehouse_id": m.warehouse_id,
                "qty": float(qty),
                "min_qty": float(m.min_qty or 0)
            })
    return out
