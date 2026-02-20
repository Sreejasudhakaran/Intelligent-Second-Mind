import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Date, DateTime
from app.db import Base


def _uuid():
    return str(uuid.uuid4())


class WeeklySummary(Base):
    __tablename__ = "weekly_summary"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, nullable=False, default="default_user")
    week_start = Column(Date)
    maintenance_pct = Column(Float, default=0.0)
    growth_pct = Column(Float, default=0.0)
    brand_pct = Column(Float, default=0.0)
    admin_pct = Column(Float, default=0.0)
    strategic_pct = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
