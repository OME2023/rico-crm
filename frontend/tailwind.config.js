/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: { borderRadius: { '2xl': '1rem' } } },
  plugins: [],
}
