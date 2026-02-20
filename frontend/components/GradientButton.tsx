"use client";

import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface GradientButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    loading?: boolean;
    loadingText?: string;
    variant?: "primary" | "secondary" | "ghost";
    size?: "sm" | "md" | "lg";
    fullWidth?: boolean;
}

const variants = {
    primary: "bg-gradient-to-r from-blue-500 to-blue-700 text-white shadow-md hover:shadow-blue-glow",
    secondary: "bg-white border border-gray-200 text-gray-700 hover:border-blue-300 hover:text-blue-600",
    ghost: "bg-transparent text-blue-500 hover:bg-blue-50",
};

const sizes = {
    sm: "px-4 py-2 text-sm rounded-lg",
    md: "px-6 py-3 text-sm rounded-xl",
    lg: "px-8 py-4 text-base rounded-xl",
};

export default function GradientButton({
    children,
    loading = false,
    loadingText,
    variant = "primary",
    size = "md",
    fullWidth = false,
    className,
    disabled,
    ...props
}: GradientButtonProps) {
    return (
        <motion.button
            whileHover={!disabled && !loading ? { y: -2 } : undefined}
            whileTap={!disabled && !loading ? { y: 0, scale: 0.99 } : undefined}
            className={cn(
                "font-semibold transition-all duration-200 flex items-center justify-center gap-2",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                variants[variant],
                sizes[size],
                fullWidth && "w-full",
                className
            )}
            disabled={disabled || loading}
            {...(props as React.HTMLAttributes<HTMLButtonElement>)}
        >
            {loading ? (
                <>
                    <Loader2 size={16} className="animate-spin" />
                    {loadingText || "Loading…"}
                </>
            ) : (
                children
            )}
        </motion.button>
    );
}
