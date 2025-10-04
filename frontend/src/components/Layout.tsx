import { Link, NavLink, Outlet } from "react-router-dom";
import { useUser } from "@/stores/user";
import { Button } from "@/components/ui/button";
import Watermark from "@/components/Watermark";

const NavItem = ({ to, label }: { to: string; label: string }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      [
        "group flex items-center gap-2 rounded-xl px-3 py-2 text-sm",
        // más contraste: blanco pleno + negrita + sombra sutil
        "text-white font-bold text-strong hover:bg-white/20 transition-colors",
        isActive ? "bg-white/30 border-l-4 border-white -ml-1 pl-2" : ""
      ].join(" ")
    }
  >
    {label}
  </NavLink>
);

export default function Layout() {
  const { name, role } = useUser();
  return (
    <div className="min-h-screen grid grid-cols-[280px_1fr]">
      <aside className="bg-sidebar text-sidebar">
        <div className="p-4">
  <Link
    to="/"
    className="block text-2xl md:text-3xl font-black leading-tight text-white text-strong"
  >
    Rico Distribución
  </Link>
  <span className="mt-1 block text-[18px] tracking-wide text-white/95 font-medium">
    Mayorista
  </span>
</div>

        <div className="px-3 pb-6 space-y-6">
          <div>
            <div className="px-2 pb-1 text-[10px] uppercase tracking-wide text-white font-bold text-strong">
              Principal
            </div>
            <nav className="space-y-1">
              <NavItem to="/" label="Dashboard" />
              <NavItem to="/products" label="Productos" />
              <NavItem to="/customers" label="Clientes" />
              <NavItem to="/suppliers" label="Proveedores" />
              <NavItem to="/sellers" label="Vendedores" />
            </nav>
          </div>

          <div>
            <div className="px-2 pb-1 text-[10px] uppercase tracking-wide text-white font-bold text-strong">
              Operaciones
            </div>
            <nav className="space-y-1">
              <NavItem to="/orders" label="Pedidos / Ventas" />
              <NavItem to="/purchases" label="Compras / Recepción" />
              <NavItem to="/stock" label="Stock" />
              <NavItem to="/price-imports" label="Listas de precios (PDF)" />
            </nav>
          </div>

          <div>
            <div className="px-2 pb-1 text-[10px] uppercase tracking-wide text-white font-bold text-strong">
              Análisis
            </div>
            <nav className="space-y-1">
              <NavItem to="/reports" label="Reportes" />
              <NavItem to="/admin" label="Administración" />
            </nav>
          </div>
        </div>
      </aside>

      <main>
        <header className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b shadow-sm flex items-center justify-between px-4 h-14">
          <div />
          <div className="flex items-center gap-3 text-sm">
            <span className="text-slate-600">{name}</span>
            <span className="rounded-full text-white px-2 py-0.5 text-xs bg-brand">
              {role}
            </span>
            <Button variant="outline">Salir</Button>
          </div>
        </header>

        {/* Contenedor relative para que el Watermark se ubique debajo del contenido */}
        <div className="relative min-h-[calc(100vh-56px)]">  {/* 56px = h-14 del header */}
  <Watermark />
  <div className="p-6 max-w-7xl mx-auto relative z-10">
    <Outlet />
  </div>
</div>
      </main>
    </div>
  );
}