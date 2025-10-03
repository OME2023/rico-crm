import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" }
});

// Si luego agregamos Auth, acá inyectamos el token:
// api.interceptors.request.use((config) => { config.headers.Authorization = `Bearer ${token}`; return config; });
