from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/todo_db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    better_auth_url: Optional[str] = None
    better_auth_secret: Optional[str] = None
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()