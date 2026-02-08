from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    database_url: str = "postgresql://user:password@localhost:5432/backend_dev"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()