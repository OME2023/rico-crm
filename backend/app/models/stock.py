from sqlalchemy import String, Integer, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Warehouse(Base):
    __tablename__ = "warehouses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

class Stock(Base):
    __tablename__ = "stock"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), index=True)
    qty_base: Mapped[float] = mapped_column(Numeric(18,6), default=0)

    __table_args__ = (
        UniqueConstraint("product_id", "warehouse_id", name="uix_stock_product_warehouse"),
    )

class StockMin(Base):
    __tablename__ = "stock_min"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), index=True)
    min_qty: Mapped[float] = mapped_column(Numeric(18,6), default=0)

    __table_args__ = (
        UniqueConstraint("product_id", "warehouse_id", name="uix_min_product_warehouse"),
    )
