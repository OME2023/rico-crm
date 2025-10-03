import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type Product = {
  id: number;
  sku: string;
  name: string;
  unit_base: string;
  factor_per_pack: number;
  supplier_id?: number | null;
  vat_override?: number | null;
  cost_net: number;
  cost_gross: number;
  price_list: number;
};

export default function Products() {
  const [data, setData] = useState<Product[]>([]);
  const [q, setQ] = useState("");

  useEffect(() => {
    api.get("/products").then(r => setData(r.data));
  }, []);

  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return data;
    return data.filter(p => `${p.sku} ${p.name}`.toLowerCase().includes(s));
  }, [data, q]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Productos</h1>
        <div className="flex gap-2">
          <Input placeholder="Buscar SKU/Nombre" value={q} onChange={e => setQ(e.target.value)} className="w-64" />
          <Button onClick={() => api.get("/products").then(r => setData(r.data))}>Refrescar</Button>
        </div>
      </div>

      <div className="overflow-auto rounded-2xl bg-white shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100">
            <tr>
              <th className="text-left p-3">SKU</th>
              <th className="text-left p-3">Nombre</th>
              <th className="text-left p-3">Unidad</th>
              <th className="text-right p-3">Costo Neto (ARS)</th>
              <th className="text-right p-3">Costo Bruto</th>
              <th className="text-right p-3">PVP Lista</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(p => (
              <tr key={p.id} className="border-t">
                <td className="p-3 font-mono">{p.sku}</td>
                <td className="p-3">{p.name}</td>
                <td className="p-3">{p.unit_base}</td>
                <td className="p-3 text-right">{p.cost_net.toFixed(2)}</td>
                <td className="p-3 text-right">{p.cost_gross.toFixed(2)}</td>
                <td className="p-3 text-right">{p.price_list.toFixed(2)}</td>
              </tr>
            ))}
            {!filtered.length && (
              <tr><td className="p-3 text-slate-500" colSpan={6}>Sin resultados</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
