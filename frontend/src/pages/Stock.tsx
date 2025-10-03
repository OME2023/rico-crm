import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type Row = { product_id: number; qty_base: number };
type Alert = { product_id: number; warehouse_id: number; qty: number; min_qty: number };

export default function Stock() {
  const [rows, setRows] = useState<Row[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [form, setForm] = useState({ product_id: "", warehouse_id: "", qty_delta: "" });

  const load = async () => {
    const [a, b] = await Promise.all([api.get("/stock"), api.get("/stock/alerts")]);
    setRows(a.data); setAlerts(b.data);
  };

  useEffect(() => { load(); }, []);

  const adjust = async () => {
    const body = {
      product_id: Number(form.product_id),
      warehouse_id: Number(form.warehouse_id),
      qty_delta: Number(form.qty_delta),
    };
    if (!body.product_id || !body.warehouse_id || !body.qty_delta) return;
    await api.post("/stock/adjust", body);
    setForm({ product_id: "", warehouse_id: "", qty_delta: "" });
    await load();
  };

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div>
        <h2 className="text-lg font-semibold mb-2">Consolidado</h2>
        <div className="rounded-2xl bg-white shadow-sm overflow-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-100">
              <tr><th className="text-left p-3">Producto</th><th className="text-right p-3">Qty base</th></tr>
            </thead>
            <tbody>
              {rows.map(r => (
                <tr key={r.product_id} className="border-t">
                  <td className="p-3">{r.product_id}</td>
                  <td className="p-3 text-right">{r.qty_base.toFixed(3)}</td>
                </tr>
              ))}
              {!rows.length && <tr><td className="p-3 text-slate-500" colSpan={2}>Sin datos</td></tr>}
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-2">Alertas de mínimos</h2>
        <div className="rounded-2xl bg-white shadow-sm overflow-auto mb-6">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-100">
              <tr>
                <th className="text-left p-3">Producto</th>
                <th className="text-left p-3">Depósito</th>
                <th className="text-right p-3">Qty</th>
                <th className="text-right p-3">Mín</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map(a => (
                <tr key={`${a.product_id}-${a.warehouse_id}`} className="border-t">
                  <td className="p-3">{a.product_id}</td>
                  <td className="p-3">{a.warehouse_id}</td>
                  <td className="p-3 text-right">{a.qty.toFixed(3)}</td>
                  <td className="p-3 text-right">{a.min_qty.toFixed(3)}</td>
                </tr>
              ))}
              {!alerts.length && <tr><td className="p-3 text-slate-500" colSpan={4}>Sin alertas</td></tr>}
            </tbody>
          </table>
        </div>

        <h2 className="text-lg font-semibold mb-2">Ajuste rápido</h2>
        <div className="flex items-center gap-2">
          <Input placeholder="product_id" value={form.product_id} onChange={e => setForm(f => ({...f, product_id: e.target.value}))} className="w-32" />
          <Input placeholder="warehouse_id" value={form.warehouse_id} onChange={e => setForm(f => ({...f, warehouse_id: e.target.value}))} className="w-32" />
          <Input placeholder="qty_delta" value={form.qty_delta} onChange={e => setForm(f => ({...f, qty_delta: e.target.value}))} className="w-32" />
          <Button onClick={adjust}>Aplicar</Button>
        </div>
      </div>
    </div>
  );
}
