import { Routes, Route } from "react-router-dom";
import Layout from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import Products from "@/pages/Products";
import Stock from "@/pages/Stock";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="/products" element={<Products />} />
        <Route path="/stock" element={<Stock />} />
        <Route path="/orders" element={<div>Pedidos (próximamente)</div>} />
        <Route path="/purchases" element={<div>Compras (próximamente)</div>} />
        <Route path="/reports" element={<div>Reportes (próximamente)</div>} />
        <Route path="/admin" element={<div>Administración (próximamente)</div>} />
      </Route>
    </Routes>
  );
}
