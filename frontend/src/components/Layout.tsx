import { Link, NavLink, Outlet } from "react-router-dom";
import { useUser } from "@/stores/user";
import { Button } from "@/components/ui/button";

const NavItem = ({ to, label }: { to: string; label: string }) => (
  <NavLink
    to={to}
    className={({isActive}) =>
      `block rounded-xl px-3 py-2 text-sm ${isActive ? "bg-slate-200 font-semibold" : "hover:bg-slate-100"}`
    }
  >
    {label}
  </NavLink>
);

export default function Layout() {
  const { name, role } = useUser();
  return (
    <div className="min-h-screen grid grid-cols-[260px_1fr]">
      <aside className="border-r bg-white">
        <div className="p-4">
          <Link to="/" className="text-xl font-bold">Rico Distribución</Link>
          <p className="text-xs text-slate-500 mt-1">CRM Mayorista</p>
        </div>
        <nav className="px-3 space-y-1">
          <NavItem to="/" label="Dashboard" />
          <NavItem to="/products" label="Productos" />
          <NavItem to="/stock" label="Stock" />
          <NavItem to="/orders" label="Pedidos" />
          <NavItem to="/purchases" label="Compras" />
          <NavItem to="/reports" label="Reportes" />
          <NavItem to="/admin" label="Administración" />
        </nav>
      </aside>

      <main className="bg-slate-50">
        <header className="sticky top-0 z-10 bg-white border-b flex items-center justify-between px-4 h-14">
          <div />
          <div className="flex items-center gap-3 text-sm">
            <span className="text-slate-600">{name}</span>
            <span className="rounded-full bg-slate-900 text-white px-2 py-0.5 text-xs">{role}</span>
            <Button variant="outline" size="sm">Salir</Button>
          </div>
        </header>
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
