from pydantic import BaseModel, ConfigDict, condecimal

class ProductIn(BaseModel):
    sku: str
    name: str
    unit_base: str
    factor_per_pack: condecimal(max_digits=18, decimal_places=6) = 1
    supplier_id: int | None = None
    vat_override: int | None = None   # si None, usar default del proveedor
    cost_net: condecimal(max_digits=18, decimal_places=4) = 0
    cost_gross: condecimal(max_digits=18, decimal_places=4) = 0
    price_list: condecimal(max_digits=18, decimal_places=4) = 0

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sku: str
    name: str
    unit_base: str
    factor_per_pack: float
    supplier_id: int | None
    vat_override: int | None
    cost_net: float
    cost_gross: float
    price_list: float
