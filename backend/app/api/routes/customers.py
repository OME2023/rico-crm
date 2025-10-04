from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Customer
from app.schemas.customers import CustomerIn  # Entrada estricta
from app.schemas.customers_safe import CustomerOutSafe  # Salida tolerante

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("", response_model=list[CustomerOutSafe])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.get("/{customer_id}", response_model=CustomerOutSafe)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(404, "Cliente no encontrado")
    return c

@router.post("", response_model=CustomerOutSafe)
def create_customer(payload: CustomerIn, db: Session = Depends(get_db)):
    c = Customer(**payload.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{customer_id}", response_model=CustomerOutSafe)
def update_customer(customer_id: int, payload: CustomerIn, db: Session = Depends(get_db)):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(404, "Cliente no encontrado")
    for k, v in payload.model_dump().items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(404, "Cliente no encontrado")
    db.delete(c); db.commit()
    return {"ok": True}
