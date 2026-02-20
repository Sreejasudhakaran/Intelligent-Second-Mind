import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime
from pgvector.sqlalchemy import Vector
from app.db import Base


def _uuid():
    return str(uuid.uuid4())


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, nullable=False, default="default_user")
    title = Column(Text, nullable=False)
    reasoning = Column(Text)
    assumptions = Column(Text)
    expected_outcome = Column(Text)
    confidence_score = Column(Integer)
    category_tag = Column(String, default="Strategy")
    embedding = Column(Vector(384))
    created_at = Column(DateTime, default=datetime.utcnow)
    review_date = Column(DateTime, nullable=True)
