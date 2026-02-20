import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from app.db import Base


def _uuid():
    return str(uuid.uuid4())


class Insight(Base):
    __tablename__ = "insights"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, nullable=False, default="default_user")
    insight_type = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
