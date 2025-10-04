import { api } from "@/lib/api";

export type Customer = {
  id: number;
  name: string;
  cuit?: string | null;
  price_list_name?: string | null;
  status: "activo" | "inactivo";
};

export const CustomersAPI = {
  list: (q?: string) => api.get<Customer[]>("/customers", { params: q ? { q } : {} }),
  create: (data: Omit<Customer, "id">) => api.post<Customer>("/customers", data),
  update: (id: number, data: Omit<Customer, "id">) => api.put<Customer>(`/customers/${id}`, data),
  remove: (id: number) => api.delete(`/customers/${id}`),
};
