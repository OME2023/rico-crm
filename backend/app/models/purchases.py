from sqlalchemy import String, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.session import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, received
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    qty_base: Mapped[float] = mapped_column(Numeric(18,6))
    cost_net: Mapped[float] = mapped_column(Numeric(18,4))
    vat_rate: Mapped[int] = mapped_column(Integer, default=21)  # 21 o 19
