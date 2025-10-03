import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function Dashboard() {
  const [alerts, setAlerts] = useState<number>(0);

  useEffect(() => {
    api.get("/stock/alerts").then(r => setAlerts(r.data.length)).catch(() => setAlerts(0));
  }, []);

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <h3 className="text-sm text-slate-500">Alertas de Stock</h3>
        <div className="text-3xl font-semibold mt-2">{alerts}</div>
        <p className="text-xs text-slate-500 mt-1">Productos por debajo de mínimos</p>
      </div>
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <h3 className="text-sm text-slate-500">Pedidos pendientes</h3>
        <div className="text-3xl font-semibold mt-2">—</div>
      </div>
      <div className="rounded-2xl bg-white p-4 shadow-sm">
        <h3 className="text-sm text-slate-500">Top clientes</h3>
        <div className="text-3xl font-semibold mt-2">—</div>
      </div>
    </div>
  );
}
