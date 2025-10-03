import os, pathlib
from fastapi.testclient import TestClient

# Usar una DB aislada para este test
os.environ["DATABASE_URL"] = "sqlite:///./test_stock.db"
# Importar después de setear env var
from app.main import app  # noqa: E402

client = TestClient(app)

def setup_module(module):
    # limpiar DB de prueba si hace falta
    p = pathlib.Path("test_stock.db")
    # Si necesitás limpiar, borrá; aquí dejamos persistir para una corrida simple.
    pass

def test_stock_flow():
    # Proveedor
    r = client.post("/suppliers", json={"name":"Test Prov","vat_default":21})
    assert r.status_code == 200
    sup = r.json()
    assert sup["vat_default"] == 21

    # Producto (hereda 21)
    r = client.post("/products", json={
        "sku":"P-001","name":"Prod","unit_base":"kg","factor_per_pack":1,
        "supplier_id": sup["id"], "cost_net":100, "cost_gross":121, "price_list":150
    })
    assert r.status_code == 200
    prod = r.json()
    assert prod["vat_override"] == 21

    # Depósito
    r = client.post("/warehouses", json={"name":"Test WH"})
    assert r.status_code == 200
    wh = r.json()

    # Ajuste +10
    r = client.post("/stock/adjust", json={"product_id": prod["id"], "warehouse_id": wh["id"], "qty_delta": 10})
    assert r.status_code == 200
    assert r.json()["ok"] is True

    # Consolidado
    r = client.get("/stock")
    assert r.status_code == 200
    rows = r.json()
    assert any(row["product_id"] == prod["id"] and float(row["qty_base"]) >= 10 for row in rows)

    # Mínimo 15 -> debe alertar
    r = client.post("/stock/min", json={"product_id": prod["id"], "warehouse_id": wh["id"], "min_qty": 15})
    assert r.status_code == 200

    r = client.get("/stock/alerts")
    assert r.status_code == 200
    alerts = r.json()
    assert any(a["product_id"] == prod["id"] and a["warehouse_id"] == wh["id"] for a in alerts)

    # Ajuste +10 -> sale de alerta
    r = client.post("/stock/adjust", json={"product_id": prod["id"], "warehouse_id": wh["id"], "qty_delta": 10})
    assert r.status_code == 200

    r = client.get("/stock/alerts")
    assert r.status_code == 200
    assert not any(a["product_id"] == prod["id"] and a["warehouse_id"] == wh["id"] for a in r.json())
