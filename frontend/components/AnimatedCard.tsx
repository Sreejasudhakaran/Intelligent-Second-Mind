"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

interface AnimatedCardProps extends Omit<HTMLMotionProps<"div">, "children"> {
    children: React.ReactNode;
    delay?: number;
    className?: string;
    hover?: boolean;
}

export default function AnimatedCard({
    children,
    delay = 0,
    className = "",
    hover = true,
    ...props
}: AnimatedCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay }}
            whileHover={hover ? { y: -2, boxShadow: "0 8px 25px rgba(0,0,0,0.08)" } : undefined}
            className={cn(
                "bg-white rounded-2xl shadow-card border border-gray-50 transition-colors duration-200",
                className
            )}
            {...props}
        >
            {children}
        </motion.div>
    );
}
