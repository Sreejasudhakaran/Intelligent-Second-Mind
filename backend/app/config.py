from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/jarvis"

    # HuggingFace
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"

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
