from pydantic import BaseModel, ConfigDict

class WarehouseIn(BaseModel):
    name: str

class WarehouseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
