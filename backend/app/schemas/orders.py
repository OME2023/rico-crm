from pydantic import BaseModel, ConfigDict, condecimal

class OrderCreateIn(BaseModel):
    customer_id: int
    discount_pct: condecimal(max_digits=5, decimal_places=2) = 0

class OrderAddItemIn(BaseModel):
    product_id: int
    warehouse_id: int
    qty_base: condecimal(max_digits=18, decimal_places=6)
    price_net: condecimal(max_digits=18, decimal_places=4)

class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    warehouse_id: int
    qty_base: float
    price_net: float
    vat_rate: int

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int
    status: str
    discount_pct: float

class OrderSummaryOut(BaseModel):
    id: int
    subtotal_net: float
    discount_pct: float
    subtotal_net_after_discount: float
    vat_21: float
    vat_19: float
    total_gross: float
