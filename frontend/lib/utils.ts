import { type ClassValue, clsx } from "clsx";

export function cn(...inputs: ClassValue[]): string {
    return inputs
        .filter(Boolean)
        .map((c) => (typeof c === "string" ? c : ""))
        .join(" ");
}

export function formatDate(dateStr?: string): string {
    if (!dateStr) return "Unknown date";
    try {
        return new Date(dateStr).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
        });
    } catch {
        return dateStr;
    }
}

export function getGreeting(): string {
    const h = new Date().getHours();
    if (h < 12) return "Good Morning";
    if (h < 17) return "Good Afternoon";
    return "Good Evening";
}

export function truncate(text: string, maxLength = 120): string {
    if (!text) return "";
    return text.length <= maxLength ? text : text.slice(0, maxLength) + "…";
}

export function clampPercent(value: number): number {
    return Math.min(100, Math.max(0, value));
}
