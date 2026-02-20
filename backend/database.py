from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/jarvis"
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"
    CORS_ORIGINS: str = "http://localhost:3000"
    DEFAULT_USER_ID: str = "default_user"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
