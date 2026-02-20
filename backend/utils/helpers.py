from datetime import datetime
from typing import Optional
from pydantic import BaseModel


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default: int = 50) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
