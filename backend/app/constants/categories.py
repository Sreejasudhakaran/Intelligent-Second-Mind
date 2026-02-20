from typing import List, Dict

# Decision category definitions with semantic descriptions
CATEGORIES: Dict[str, str] = {
    "Revenue Growth": "sales revenue growth business expansion monetization income profit",
    "Maintenance": "maintenance fixing bugs technical debt infrastructure upkeep repairs",
    "Brand": "branding marketing awareness content social media presence reputation",
    "Admin": "administration meetings planning organization HR legal compliance",
    "Strategy": "strategy vision long-term planning goals direction innovation transformation",
}

CATEGORY_COLORS: Dict[str, str] = {
    "Revenue Growth": "#3B82F6",  # Blue
    "Maintenance": "#9CA3AF",     # Gray
    "Brand": "#A855F7",           # Purple
    "Admin": "#F59E0B",           # Orange
    "Strategy": "#22C55E",        # Green
}

CATEGORY_LIST: List[str] = list(CATEGORIES.keys())
