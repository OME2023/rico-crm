from pydantic import BaseModel, ConfigDict
class SupplierIn(BaseModel):
    name: str
    vat_default: int = 21  # 21 o 19

class SupplierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    vat_default: int
