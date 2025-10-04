from sqlalchemy import String, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.session import Base

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(String(20), default="cart")  # cart, confirmed, invoiced
    discount_pct: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("sales_orders.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
    qty_base: Mapped[float] = mapped_column(Numeric(18,6))
    price_net: Mapped[float] = mapped_column(Numeric(18,4))  # precio neto unitario
    vat_rate: Mapped[int] = mapped_column(Integer, default=21) # 21 o 19
