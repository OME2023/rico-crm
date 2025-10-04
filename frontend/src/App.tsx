import { Routes, Route } from "react-router-dom";
import Layout from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import Products from "@/pages/Products";
import Stock from "@/pages/Stock";
import Customers from "@/pages/Customers";
import Suppliers from "@/pages/Suppliers";
import Sellers from "@/pages/Sellers";
import Orders from "@/pages/Orders";
import Purchases from "@/pages/Purchases";
import Reports from "@/pages/Reports";
import Admin from "@/pages/Admin";
import PriceImports from "@/pages/PriceImports";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="/products" element={<Products />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/suppliers" element={<Suppliers />} />
        <Route path="/sellers" element={<Sellers />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/purchases" element={<Purchases />} />
        <Route path="/stock" element={<Stock />} />
        <Route path="/price-imports" element={<PriceImports />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/admin" element={<Admin />} />
      </Route>
    </Routes>
  );
}
