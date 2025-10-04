from typing import Optional
from pydantic import BaseModel, ConfigDict

class CustomerOutSafe(BaseModel):
    id: int
    name: str
    dni: Optional[str] = None
    phone: Optional[str] = None
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_floor: Optional[str] = None
    address_apartment: Optional[str] = None
    neighborhood: Optional[str] = None
    cuit: Optional[str] = None
    fiscal_condition: Optional[str] = None
    price_list_name: Optional[str] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
