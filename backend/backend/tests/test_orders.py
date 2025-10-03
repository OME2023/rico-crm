import os, pathlib

# Asegurar DB limpia antes de importar la app
DB = "test_orders.db"
if pathlib.Path(DB).exists():
    os.remove(DB)
os.environ["DATABASE_URL"] = f"sqlite:///./{DB}"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_order_flow():
    # Cliente
    r = client.post("/customers", json={"name":"C1"})
    assert r.status_code == 200
    cid = r.json()["id"]

    # Proveedor + Producto
    r = client.post("/suppliers", json={"name":"Prov","vat_default":21}); assert r.status_code==200
    r = client.post("/products", json={"sku":"PX-1","name":"Prod X","unit_base":"kg","factor_per_pack":1,"supplier_id":1,"cost_net":100,"cost_gross":121,"price_list":150})
    assert r.status_code in (200,201)
    pid = r.json()["id"]

    # Depósito + Stock
    r = client.post("/warehouses", json={"name":"W1"}); assert r.status_code==200
    wid = r.json()["id"]
    r = client.post("/stock/adjust", json={"product_id": pid, "warehouse_id": wid, "qty_delta": 10}); assert r.status_code==200

    # Pedido con 10% descuento
    r = client.post("/orders", json={"customer_id": cid, "discount_pct": 10}); assert r.status_code==201
    oid = r.json()["id"]

    # Agregar 2 unidades a 100 neto
    r = client.post(f"/orders/{oid}/add", json={"product_id": pid, "warehouse_id": wid, "qty_base": 2, "price_net": 100})
    assert r.status_code==200

    # Summary
    r = client.get(f"/orders/{oid}/summary"); assert r.status_code==200
    s = r.json()
    assert round(s["subtotal_net"],2) == 200.00
    assert round(s["subtotal_net_after_discount"],2) == 180.00  # 10% off
    assert round(s["vat_21"],2) == 42.00
    assert round(s["total_gross"],2) == 222.00

    # Confirmar y verificar stock descontado
    r = client.post(f"/orders/{oid}/confirm"); assert r.status_code==200
    r = client.get("/stock"); assert r.status_code==200
    consolidated = r.json()
    found = False
    for row in consolidated:
        if row["product_id"] == pid:
            found = True
            assert float(row["qty_base"]) == 8.0
    assert found
