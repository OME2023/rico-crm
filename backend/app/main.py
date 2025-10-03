from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health import router as health_router
from app.db.session import Base, engine

# Crea tablas (MVP); luego usaremos Alembic para migraciones formales
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rico Distribución API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
