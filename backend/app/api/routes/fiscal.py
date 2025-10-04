import os
from fastapi import APIRouter, HTTPException, Query
from app.core.cuit import normalize_cuit

router = APIRouter(prefix="/fiscal", tags=["fiscal"])

@router.get("/lookup")
def lookup_fiscal(cuit: str = Query(..., description="CUIT con o sin guiones")):
    norm = normalize_cuit(cuit)
    if not norm:
        raise HTTPException(400, "CUIT inválido")
    # Demo: responder fijo si está habilitado
    if os.getenv("DEMO_FISCAL_FAKE") == "1":
        return {"cuit": norm, "fiscal_condition": "Responsable Inscripto"}
    raise HTTPException(501, "Lookup fiscal no configurado")
