from pydantic import BaseModel, ConfigDict

class CustomerIn(BaseModel):
    name: str
    cuit: str | None = None
    price_list_name: str | None = None

class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    cuit: str | None = None
    price_list_name: str | None = None
    status: str
