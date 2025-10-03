from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.core import Supplier, VATRate
from app.schemas.suppliers import SupplierIn, SupplierOut

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.get("", response_model=list[SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).order_by(Supplier.id.desc()).all()

@router.post("", response_model=SupplierOut)
def create_supplier(payload: SupplierIn, db: Session = Depends(get_db)):
    if payload.vat_default not in (21, 19):
        raise HTTPException(400, "vat_default debe ser 21 o 19")
    s = Supplier(name=payload.name, vat_default=VATRate.IVA_21 if payload.vat_default==21 else VATRate.IVA_19)
    db.add(s); db.commit(); db.refresh(s)
    return s
