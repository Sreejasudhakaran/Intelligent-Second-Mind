import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from app.db import Base


def _uuid():
    return str(uuid.uuid4())


class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(String, primary_key=True, default=_uuid)
    decision_id = Column(String, ForeignKey("decisions.id", ondelete="CASCADE"))
    actual_outcome = Column(Text)
    lessons = Column(Text)
    accuracy_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
