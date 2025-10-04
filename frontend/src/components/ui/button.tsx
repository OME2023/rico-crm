import * as React from "react";

type Variant = "primary" | "secondary" | "danger";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
};

const classesByVariant: Record<Variant, string> = {
  // Verde de marca (ajustá el hex si querés afinar el tono)
  primary:
    "bg-[#7DBB42] text-white hover:brightness-95 focus:ring-[#7DBB42]/30",
  secondary:
    "bg-white text-slate-900 border border-slate-200 hover:bg-slate-50 focus:ring-slate-200",
  danger:
    "bg-red-600 text-white hover:bg-red-700 focus:ring-red-200",
};

export function Button({
  variant = "secondary",
  className = "",
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center rounded-2xl px-5 py-2.5 text-sm font-medium transition-colors " +
    "focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  return (
    <button
      className={`${base} ${classesByVariant[variant]} ${className}`}
      {...props}
    />
  );
}
