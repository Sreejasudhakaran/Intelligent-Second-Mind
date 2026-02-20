export const CATEGORIES = [
    "Revenue Growth",
    "Maintenance",
    "Brand",
    "Admin",
    "Strategy",
] as const;

export type Category = (typeof CATEGORIES)[number];

export const CATEGORY_DESCRIPTIONS: Record<Category, string> = {
    "Revenue Growth": "Sales, monetization, business expansion",
    Maintenance: "Bug fixes, technical debt, upkeep",
    Brand: "Marketing, content, awareness",
    Admin: "Meetings, planning, HR, legal",
    Strategy: "Vision, long-term goals, innovation",
};

export const CATEGORY_ICONS: Record<Category, string> = {
    "Revenue Growth": "📈",
    Maintenance: "🔧",
    Brand: "🎨",
    Admin: "📋",
    Strategy: "🎯",
};
