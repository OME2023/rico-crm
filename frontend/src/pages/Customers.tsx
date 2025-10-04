import { useEffect, useMemo, useState } from "react";
import { CustomersAPI, type Customer } from "@/lib/customers";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Modal from "@/components/ui/modal";

type FormState = {
  name: string;
  cuit?: string;
  price_list_name?: string;
  status: "activo" | "inactivo";
};

export default function Customers() {
  const [items, setItems] = useState<Customer[]>([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [editId, setEditId] = useState<number | undefined>(undefined);
  const [form, setForm] = useState<FormState>({
    name: "", cuit: "", price_list_name: "", status: "activo",
  });

  const filtered = useMemo(() => {
    if (!q) return items;
    const t = q.toLowerCase();
    return items.filter(x =>
      x.name.toLowerCase().includes(t) || (x.cuit || "").toLowerCase().includes(t)
    );
  }, [items, q]);

  const load = () => {
    setLoading(true);
    CustomersAPI.list().then(r => setItems(r.data)).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const startCreate = () => {
    setEditId(undefined);
    setForm({ name: "", cuit: "", price_list_name: "", status: "activo" });
    setOpen(true);
  };
  const startEdit = (c: Customer) => {
    setEditId(c.id);
    setForm({
      name: c.name,
      cuit: c.cuit || "",
      price_list_name: c.price_list_name || "",
      status: c.status,
    });
    setOpen(true);
  };

  const save = async () => {
    if (!form.name.trim()) return alert("Nombre es requerido");
    const payload = {
      ...form,
      cuit: form.cuit || undefined,
      price_list_name: form.price_list_name || undefined,
    };
    if (editId) {
      const r = await CustomersAPI.update(editId, payload as any);
      setItems(arr => arr.map(x => (x.id === editId ? r.data : x)));
    } else {
      const r = await CustomersAPI.create(payload as any);
      setItems(arr => [r.data, ...arr]);
    }
    setOpen(false);
  };

  const remove = async (id: number) => {
    if (!confirm("¿Eliminar cliente?")) return;
    await CustomersAPI.remove(id);
    setItems(arr => arr.filter(x => x.id !== id));
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Clientes</h1>
        <div className="flex items-center gap-2">
          <Input
            placeholder="Buscar por nombre o CUIT…"
            value={q}
            onChange={e => setQ(e.target.value)}
            className="w-64"
          />
          <Button onClick={startCreate}>Nuevo</Button>
          <Button variant="outline" onClick={load}>Refrescar</Button>
        </div>
      </div>

      <div className="rounded-2xl border bg-white shadow-sm overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <th className="text-left px-4 py-2">Nombre</th>
              <th className="text-left px-4 py-2">CUIT</th>
              <th className="text-left px-4 py-2">Lista</th>
              <th className="text-left px-4 py-2">Estado</th>
              <th className="px-4 py-2 w-32"></th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                  Cargando…
                </td>
              </tr>
            )}
            {!loading && filtered.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                  Sin resultados
                </td>
              </tr>
            )}
            {filtered.map(c => (
              <tr key={c.id} className="border-t hover:bg-slate-50/60">
                <td className="px-4 py-2 font-medium">{c.name}</td>
                <td className="px-4 py-2">{c.cuit || "—"}</td>
                <td className="px-4 py-2">{c.price_list_name || "—"}</td>
                <td className="px-4 py-2">
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs text-white ${
                      c.status === "activo" ? "bg-emerald-500" : "bg-slate-400"
                    }`}
                  >
                    {c.status}
                  </span>
                </td>
                <td className="px-4 py-2 text-right space-x-2">
                  <Button variant="outline" onClick={() => startEdit(c)}>Editar</Button>
                  <Button variant="outline" onClick={() => remove(c.id)}>Borrar</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal open={open} onClose={() => setOpen(false)}>
        <h2 className="text-lg font-semibold mb-4">
          {editId ? "Editar cliente" : "Nuevo cliente"}
        </h2>
        <div className="space-y-3">
          <div>
            <label className="block text-xs text-slate-600 mb-1">Nombre *</label>
            <Input
              value={form.name}
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-slate-600 mb-1">CUIT</label>
              <Input
                value={form.cuit || ""}
                onChange={e => setForm(f => ({ ...f, cuit: e.target.value }))}
                placeholder="20-12345678-9"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-600 mb-1">Lista de precios</label>
              <Input
                value={form.price_list_name || ""}
                onChange={e => setForm(f => ({ ...f, price_list_name: e.target.value }))}
                placeholder="Mayorista A"
              />
            </div>
          </div>
          <div>
            <label className="block text-xs text-slate-600 mb-1">Estado</label>
            <select
              value={form.status}
              onChange={e =>
                setForm(f => ({ ...f, status: e.target.value as "activo" | "inactivo" }))
              }
              className="w-full h-10 rounded-xl border px-3"
            >
              <option value="activo">activo</option>
              <option value="inactivo">inactivo</option>
            </select>
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="outline" onClick={() => setOpen(false)}>Cancelar</Button>
            <Button onClick={save}>{editId ? "Guardar" : "Crear"}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
