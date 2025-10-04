import { create } from "zustand";
export type Role = "admin" | "ventas" | "compras" | "deposito";
type UserState = { name: string; role: Role; set: (u: Partial<UserState>) => void };
export const useUser = create<UserState>((set) => ({
  name: "Invitado",
  role: "admin",
  set: (u) => set(u),
}));
