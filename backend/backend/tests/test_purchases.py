import os, pathlib

DB = "test_purchases.db"
if pathlib.Path(DB).exists():
    os.remove(DB)
os.environ["DATABASE_URL"] = f"sqlite:///./{DB}"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_receive_updates_stock_and_avg_cost():
    # Proveedor, depósito
    r = client.post("/suppliers", json={"name":"Prov","vat_default":21}); assert r.status_code==200
    r = client.post("/warehouses", json={"name":"WH1"}); assert r.status_code==200
    wid = r.json()["id"]

    # Producto con costo inicial 100 y stock 20
    r = client.post("/products", json={"sku":"AVG-1","name":"Avg Test","unit_base":"kg","factor_per_pack":1,"supplier_id":1,"cost_net":100,"cost_gross":121,"price_list":150})
    assert r.status_code in (200,201)
    pid = r.json()["id"]
    r = client.post("/stock/adjust", json={"product_id": pid, "warehouse_id": wid, "qty_delta": 20}); assert r.status_code==200

    # OC: recibo 10 a 80
    r = client.post("/purchases", json={"supplier_id":1}); assert r.status_code==201
    poid = r.json()["id"]
    r = client.post(f"/purchases/{poid}/add", json={"product_id": pid, "warehouse_id": wid, "qty_base": 10, "cost_net": 80, "vat_rate": 21}); assert r.status_code==200
    r = client.post(f"/purchases/{poid}/receive"); assert r.status_code==200

    # Stock total: 30
    r = client.get("/stock"); assert r.status_code==200
    total = next(x for x in r.json() if x["product_id"]==pid)["qty_base"]
    assert float(total) == 30.0

    # Costo promedio: (20*100 + 10*80)/30 = 93.333...
    r = client.get("/products"); assert r.status_code==200
    prod = next(x for x in r.json() if x["id"]==pid)
    assert round(float(prod["cost_net"]),2) == 93.33

    # Auditoría tiene al menos 2 registros
    r = client.get("/audit"); assert r.status_code==200
    logs = r.json()
    assert any(l["action"]=="stock_increase" for l in logs)
    assert any(l["action"]=="cost_avg_update" for l in logs)
