from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.api.routes.suppliers import router as suppliers_router
from app.api.routes.products import router as products_router
from app.db.session import Base, engine

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
