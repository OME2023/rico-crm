import * as React from "react";
import { cn } from "@/lib/cn";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-100 active:scale-[.98] transition",
        className
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
