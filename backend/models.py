from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid
from database import engine

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, default="default_user")
    title = Column(Text, nullable=False)
    reasoning = Column(Text)
    assumptions = Column(Text)
    expected_outcome = Column(Text)
    confidence_score = Column(Integer)
    category_tag = Column(String)
    embedding = Column(Vector(384))
    created_at = Column(DateTime, default=datetime.utcnow)
    review_date = Column(DateTime, nullable=True)

    reflections = relationship("Reflection", back_populates="decision")


class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(String, primary_key=True, default=generate_uuid)
    decision_id = Column(String, ForeignKey("decisions.id"))
    actual_outcome = Column(Text)
    lessons = Column(Text)
    accuracy_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    decision = relationship("Decision", back_populates="reflections")


class WeeklySummary(Base):
    __tablename__ = "weekly_summary"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, default="default_user")
    week_start = Column(DateTime)
    maintenance_pct = Column(Float)
    growth_pct = Column(Float)
    brand_pct = Column(Float)
    admin_pct = Column(Float)
    strategic_pct = Column(Float)


class Insight(Base):
    __tablename__ = "insights"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, default="default_user")
    insight_type = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)
