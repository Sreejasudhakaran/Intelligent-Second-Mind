from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Supabase requires SSL. connect_args ensures psycopg2 uses SSL even if
# the URL doesn't contain ?sslmode=require (handles Windows DNS quirks too).
_connect_args = {}
if "supabase" in settings.DATABASE_URL:
    _connect_args = {"sslmode": "require"}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args=_connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    """Create all SQLAlchemy-mapped tables."""
    # Import all models to register them with Base.metadata
    from app.models import decision, reflection, weekly_summary, insight  # noqa
    Base.metadata.create_all(bind=engine)
