import logoOrange from "@/assets/logo-orange.png";

/**
 * Marca de agua NARANJA centrada en el área de contenido.
 * - Usa import para que Vite resuelva el asset.
 * - Va en z-0 dentro de un contenedor relative; el contenido va en z-10.
 */
export default function Watermark() {
  return (
    <div className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-0">
      <img
        src="/logo-orange.png"   // en public/
        alt=""
        className="w-[860px] max-w-[85vw] opacity-25"  // podés subir/bajar tamaño u opacidad
      />
    </div>
  );
}