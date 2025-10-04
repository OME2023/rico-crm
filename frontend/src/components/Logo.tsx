export default function Logo({ size=44, variant="orange" }: { size?: number; variant?: "orange"|"green" }) {
  const src = variant === "green" ? "/src/assets/logo-green.png" : "/src/assets/logo-orange.png";
  return <img src={src} alt="Rico Distribución" style={{ width: size, height: size, objectFit: "contain" }} />;
}
