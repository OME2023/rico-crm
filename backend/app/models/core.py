from enum import Enum as PyEnum
from sqlalchemy import String, Integer, ForeignKey, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class VATRate(PyEnum):
    IVA_21 = 21
    IVA_19 = 19

class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    vat_default: Mapped[VATRate] = mapped_column(Enum(VATRate), default=VATRate.IVA_21)

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    unit_base: Mapped[str] = mapped_column(String(20))  # kg, caja, litro
    factor_per_pack: Mapped[float] = mapped_column(Numeric(18,6), default=1)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"))
    supplier: Mapped[Supplier | None] = relationship("Supplier")
    vat_override: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 21 o 19
    cost_net: Mapped[float] = mapped_column(Numeric(18,4), default=0)
    cost_gross: Mapped[float] = mapped_column(Numeric(18,4), default=0)
    price_list: Mapped[float] = mapped_column(Numeric(18,4), default=0)
