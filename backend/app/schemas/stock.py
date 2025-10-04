from pydantic import BaseModel, ConfigDict, condecimal

class StockAdjustIn(BaseModel):
    product_id: int
    warehouse_id: int
    qty_delta: condecimal(max_digits=18, decimal_places=6)

class StockMinSetIn(BaseModel):
    product_id: int
    warehouse_id: int
    min_qty: condecimal(max_digits=18, decimal_places=6)

class StockRowOut(BaseModel):
    product_id: int
    qty_base: float

class StockAlertOut(BaseModel):
    product_id: int
    warehouse_id: int
    qty: float
    min_qty: float
