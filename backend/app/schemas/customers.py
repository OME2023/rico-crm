from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

# -------- Input --------
class CustomerIn(BaseModel):
    name: str
    dni: Optional[str] = None
    phone: Optional[str] = None

    # Acepta tanto alias cortos como los nombres del modelo
    address_street: Optional[str] = Field(None, alias="street")
    address_number: Optional[str] = Field(None, alias="number")
    address_floor: Optional[str] = Field(None, alias="floor")
    address_apartment: Optional[str] = Field(None, alias="apartment")
    neighborhood: Optional[str] = None

    cuit: Optional[str] = None
    fiscal_condition: Optional[str] = Field(None, alias="fiscalCondition")
    price_list_name: Optional[str] = Field(None, alias="priceListName")

    model_config = ConfigDict(populate_by_name=True)

# -------- Output --------
class CustomerOut(BaseModel):
    id: int
    name: str
    dni: Optional[str]
    phone: Optional[str]
    address_street: Optional[str]
    address_number: Optional[str]
    address_floor: Optional[str]
    address_apartment: Optional[str]
    neighborhood: Optional[str]
    cuit: Optional[str]
    fiscal_condition: Optional[str]
    price_list_name: Optional[str]
    status: str

    model_config = ConfigDict(from_attributes=True)
