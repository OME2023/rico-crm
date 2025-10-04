from pydantic import BaseModel, ConfigDict, condecimal

class PurchaseCreateIn(BaseModel):
    supplier_id: int

class PurchaseAddItemIn(BaseModel):
    product_id: int
    warehouse_id: int
    qty_base: condecimal(max_digits=18, decimal_places=6)
    cost_net: condecimal(max_digits=18, decimal_places=4)
    vat_rate: int = 21

class PurchaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    supplier_id: int
    status: str

class PurchaseItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    product_id: int
    warehouse_id: int
    qty_base: float
    cost_net: float
    vat_rate: int
