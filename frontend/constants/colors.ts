export const COLORS = {
    // Primary
    blue: "#3B82F6",
    blueDark: "#2563EB",
    blueLight: "#60A5FA",

    // Backgrounds
    bgFrom: "#EEF4FF",
    bgTo: "#F8FAFF",
    card: "#FFFFFF",

    // Semantic
    green: "#22C55E",
    orange: "#F59E0B",
    purple: "#A855F7",
    gray: "#E5E7EB",

    // Text
    textDark: "#1F2937",
    textSecondary: "#6B7280",
    textMuted: "#9CA3AF",
} as const;

export const CATEGORY_COLORS: Record<string, string> = {
    "Revenue Growth": COLORS.blue,
    Maintenance: "#9CA3AF",
    Brand: COLORS.purple,
    Admin: COLORS.orange,
    Strategy: COLORS.green,
};

export const PROGRESS_BAR_COLORS: Record<string, string> = {
    "Revenue Growth": "bg-blue-500",
    Maintenance: "bg-gray-400",
    Brand: "bg-purple-400",
    Admin: "bg-orange-400",
    Strategy: "bg-green-500",
};
