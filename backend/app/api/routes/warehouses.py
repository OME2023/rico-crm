from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.stock import Warehouse
from app.schemas.warehouses import WarehouseIn, WarehouseOut

router = APIRouter(prefix="/warehouses", tags=["warehouses"])

@router.get("", response_model=list[WarehouseOut])
def list_warehouses(db: Session = Depends(get_db)):
    return db.query(Warehouse).order_by(Warehouse.id.desc()).all()

@router.post("", response_model=WarehouseOut)
def create_warehouse(payload: WarehouseIn, db: Session = Depends(get_db)):
    if db.query(Warehouse).filter(Warehouse.name==payload.name).first():
        raise HTTPException(400, "Ya existe un depósito con ese nombre")
    w = Warehouse(name=payload.name)
    db.add(w); db.commit(); db.refresh(w)
    return w
