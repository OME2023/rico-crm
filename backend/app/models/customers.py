from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    cuit: Mapped[str | None] = mapped_column(String(20), index=True, default=None)
    price_list_name: Mapped[str | None] = mapped_column(String(50), default=None)
    status: Mapped[str] = mapped_column(String(20), default="activo")
