from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.core import Product, Supplier, VATRate
from app.schemas.products import ProductIn, ProductOut

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=list[ProductOut])
def list_products(q: str | None = None, db: Session = Depends(get_db)):
    qry = db.query(Product)
    if q:
        ql = f"%{q}%"
        qry = qry.filter((Product.sku.ilike(ql)) | (Product.name.ilike(ql)))
    return qry.order_by(Product.id.desc()).limit(200).all()

@router.post("", response_model=ProductOut)
def create_product(payload: ProductIn, db: Session = Depends(get_db)):
    data = payload.model_dump()
    # Regla IVA: si no hay override y hay proveedor, tomar el default del proveedor
    if data.get("vat_override") is None and data.get("supplier_id"):
        supplier = db.get(Supplier, data["supplier_id"])
        if not supplier:
            raise HTTPException(400, "Proveedor no existe")
        data["vat_override"] = int((supplier.vat_default or VATRate.IVA_21).value)
    p = Product(**data)
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductIn, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    data = payload.model_dump()
    if data.get("vat_override") is None and data.get("supplier_id"):
        supplier = db.get(Supplier, data["supplier_id"])
        if not supplier:
            raise HTTPException(400, "Proveedor no existe")
        data["vat_override"] = int((supplier.vat_default or VATRate.IVA_21).value)
    for k,v in data.items():
        setattr(p, k, v)
    db.commit(); db.refresh(p)
    return p

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    db.delete(p); db.commit()
    return {"ok": True}
