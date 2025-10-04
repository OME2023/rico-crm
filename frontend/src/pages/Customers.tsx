import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";

type Customer = {
  id: number;
  name: string;
  dni: string | null;
  phone: string | null;
  address_street: string | null;
  address_number: string | null;
  address_floor: string | null;
  address_apartment: string | null;
  neighborhood: string | null;
  cuit: string;
  fiscal_condition: string | null;
  price_list_name: string | null;
  status?: string | null;
};

const FISCALES = [
  "Consumidor Final",
  "Monotributista",
  "Responsable Inscripto",
  "Exento",
  "SAS",
  "S.R.L",
  "S.A",
  "S.H",
];

const PRICE_LISTS = ["Mayorista", "Minorista"];

export default function Customers() {
  const [data, setData] = useState<Customer[]>([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);

  const [editing, setEditing] = useState<Customer | null>(null);
  const [form, setForm] = useState<Partial<Customer>>({});

  const filtered = useMemo(() => {
    const k = q.trim().toLowerCase();
    if (!k) return data;
    return data.filter((c) =>
      [
        c.name,
        c.cuit,
        c.dni ?? "",
        c.neighborhood ?? "",
        c.phone ?? "",
      ]
        .join(" ")
        .toLowerCase()
        .includes(k)
    );
  }, [q, data]);

  function openEdit(c: Customer) {
    setEditing(c);
    setForm({
      ...c,
      price_list_name: c.price_list_name ?? "",
      fiscal_condition: c.fiscal_condition ?? "",
      dni: c.dni ?? "",
      phone: c.phone ?? "",
      address_street: c.address_street ?? "",
      address_number: c.address_number ?? "",
      address_floor: c.address_floor ?? "",
      address_apartment: c.address_apartment ?? "",
      neighborhood: c.neighborhood ?? "",
    });
  }

  function closeEdit() {
    setEditing(null);
    setForm({});
  }

  async function load() {
    setLoading(true);
    try {
      const r = await api.get("/customers");
      setData(r.data);
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    if (!editing) return;
    const payload = {
      name: form.name?.trim() ?? "",
      dni: (form.dni ?? "") || null,
      phone: (form.phone ?? "") || null,
      address_street: (form.address_street ?? "") || null,
      address_number: (form.address_number ?? "") || null,
      address_floor: (form.address_floor ?? "") || null,
      address_apartment: (form.address_apartment ?? "") || null,
      neighborhood: (form.neighborhood ?? "") || null,
      cuit: (form.cuit ?? editing.cuit).replaceAll("-", ""),
      fiscal_condition: (form.fiscal_condition ?? "") || null,
      price_list_name: (form.price_list_name ?? "") || null,
      status: form.status ?? editing.status ?? "activo",
    };

    const r = await api.put(`/customers/${editing.id}`, payload);
    // merge en memoria
    setData((arr) =>
      arr.map((x) => (x.id === editing.id ? { ...x, ...r.data } : x))
    );
    closeEdit();
  }

  async function remove(id: number) {
    if (!confirm("¿Eliminar este cliente?")) return;
    await api.delete(`/customers/${id}`);
    setData((arr) => arr.filter((x) => x.id !== id));
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="p-6 lg:p-8">
      {/* search + actions */}
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar nombre, CUIT, DNI, barrio..."
          className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none ring-0 placeholder:text-slate-400 sm:max-w-xl"
        />
        <div className="flex gap-3">
          <Button variant="primary" onClick={() => alert("Alta rápida próximamente")}>
            + Nuevo cliente
          </Button>
          <Button onClick={load}>Refrescar</Button>
        </div>
      </div>

      <h1 className="mb-4 text-3xl font-bold tracking-tight text-slate-900">Clientes</h1>

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
        <table className="min-w-full text-left">
          <thead className="bg-slate-50 text-slate-500">
            <tr className="text-sm">
              <th className="px-5 py-3 font-medium">Nombre</th>
              <th className="px-5 py-3 font-medium">CUIT</th>
              <th className="px-5 py-3 font-medium">DNI</th>
              <th className="px-5 py-3 font-medium">Teléfono</th>
              <th className="px-5 py-3 font-medium">Barrio</th>
              <th className="px-5 py-3 font-medium">Cond. Fiscal</th>
              <th className="px-5 py-3 font-medium">Lista</th>
              <th className="px-5 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-800">
            {loading && (
              <tr>
                <td className="px-5 py-5 text-sm" colSpan={8}>
                  Cargando...
                </td>
              </tr>
            )}
            {!loading &&
              filtered.map((c) => (
                <tr key={c.id} className="text-sm">
                  <td className="px-5 py-4">{c.name}</td>
                  <td className="px-5 py-4">{c.cuit}</td>
                  <td className="px-5 py-4">{c.dni ?? "—"}</td>
                  <td className="px-5 py-4">{c.phone ?? "—"}</td>
                  <td className="px-5 py-4">{c.neighborhood ?? "—"}</td>
                  <td className="px-5 py-4">{c.fiscal_condition ?? "—"}</td>
                  <td className="px-5 py-4">{c.price_list_name ?? "—"}</td>
                  <td className="px-5 py-4">
                    <div className="flex gap-2">
                      <Button onClick={() => openEdit(c)}>Editar</Button>
                      <Button variant="danger" onClick={() => remove(c.id)}>
                        Eliminar
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            {!loading && filtered.length === 0 && (
              <tr>
                <td className="px-5 py-7 text-sm text-slate-500" colSpan={8}>
                  No se encontraron clientes.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Modal de edición */}
      {editing && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-3">
          <div className="w-[95vw] max-w-4xl rounded-3xl bg-white p-6 shadow-xl sm:p-7">
            <div className="mb-6 flex items-start justify-between gap-4">
              <h2 className="text-2xl font-bold text-slate-900">Editar cliente</h2>
              <button
                className="rounded-full border border-slate-200 p-2 hover:bg-slate-50"
                onClick={closeEdit}
                aria-label="Cerrar"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
              {/* Nombre */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Nombre y Apellido *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.name ?? ""}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                />
              </div>

              {/* DNI */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">DNI *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.dni ?? ""}
                  onChange={(e) => setForm((f) => ({ ...f, dni: e.target.value }))}
                />
              </div>

              {/* Teléfono */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Teléfono *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.phone ?? ""}
                  onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))}
                />
              </div>

              {/* Calle */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Calle *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.address_street ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, address_street: e.target.value }))
                  }
                />
              </div>

              {/* Número */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Número *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.address_number ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, address_number: e.target.value }))
                  }
                />
              </div>

              {/* Piso */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Piso</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.address_floor ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, address_floor: e.target.value }))
                  }
                />
              </div>

              {/* Depto */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Depto</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.address_apartment ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, address_apartment: e.target.value }))
                  }
                />
              </div>

              {/* Barrio */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Barrio *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.neighborhood ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, neighborhood: e.target.value }))
                  }
                />
              </div>

              {/* CUIT */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">CUIT *</label>
                <input
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.cuit ?? editing.cuit}
                  onChange={(e) => setForm((f) => ({ ...f, cuit: e.target.value }))}
                />
              </div>

              {/* Condición Fiscal */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Condición Fiscal *</label>
                <select
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.fiscal_condition ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, fiscal_condition: e.target.value }))
                  }
                >
                  <option value="">Seleccionar...</option>
                  {FISCALES.map((x) => (
                    <option key={x} value={x}>
                      {x}
                    </option>
                  ))}
                </select>
              </div>

              {/* Lista de precios */}
              <div className="flex flex-col">
                <label className="mb-1 text-sm text-slate-600">Lista de precios *</label>
                <select
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none"
                  value={form.price_list_name ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, price_list_name: e.target.value }))
                  }
                >
                  <option value="">Seleccionar...</option>
                  {PRICE_LISTS.map((x) => (
                    <option key={x} value={x}>
                      {x}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* acciones */}
            <div className="mt-7 flex flex-wrap justify-end gap-3">
              <Button onClick={closeEdit}>Cancelar</Button>
              <Button variant="primary" onClick={save}>
                Guardar
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
