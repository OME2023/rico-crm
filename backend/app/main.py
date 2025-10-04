from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.suppliers import router as suppliers_router
from app.api.routes.products import router as products_router
from app.api.routes.warehouses import router as warehouses_router
from app.api.routes.stock import router as stock_router
from app.api.routes.customers import router as customers_router
from app.api.routes.orders import router as orders_router
from app.api.routes.purchases import router as purchases_router
from app.api.routes.audit import router as audit_router
from app.db.session import Base, engine
from app.api.routes import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rico Distribución API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(suppliers_router)
app.include_router(products_router)
app.include_router(warehouses_router)
app.include_router(stock_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(purchases_router)
app.include_router(audit_router)
