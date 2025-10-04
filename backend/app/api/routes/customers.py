from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.customers import Customer
from app.schemas.customers import CustomerIn, CustomerOut

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).order_by(Customer.id.desc()).all()

@router.post("", response_model=CustomerOut)
def create_customer(payload: CustomerIn, db: Session = Depends(get_db)):
    c = Customer(**payload.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c
