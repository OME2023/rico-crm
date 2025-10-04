from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    # Identificación
    dni = Column(String(20), nullable=True)
    cuit = Column(String(20), nullable=True)

    # Contacto
    phone = Column(String(30), nullable=True)

    # Dirección
    address_street = Column(String(120), nullable=True)
    address_number = Column(String(30), nullable=True)
    address_floor = Column(String(20), nullable=True)
    address_apartment = Column(String(20), nullable=True)
    neighborhood = Column(String(80), nullable=True)

    # Fiscal y comercial
    fiscal_condition = Column(String(60), nullable=True)
    price_list_name = Column(String(80), nullable=True)

    # Estado opcional
    status = Column(String(20), nullable=True)
