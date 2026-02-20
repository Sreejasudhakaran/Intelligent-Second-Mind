from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/jarvis"

    # HuggingFace local model settings
    # Embedding model (used by embedding_service.py)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    # LLM model (used locally by llm_service.py)
    LLM_MODEL: str = "google/flan-t5-base"

    # App
    APP_ENV: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"
    DEFAULT_USER_ID: str = "default_user"

    # Auth (optional JWT)
    SECRET_KEY: str = "jarvis-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
