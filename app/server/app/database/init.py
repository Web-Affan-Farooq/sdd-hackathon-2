from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from ..config.settings import settings


def get_async_database_url(url: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg://"""
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


async def create_db_and_tables() -> None:
    """Create all database tables."""
    from .database import engine  # Import here to avoid circular imports

    async with engine.begin() as conn:
        # Create all tables defined in SQLModel metadata
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db_and_tables() -> None:
    """Drop all database tables (use with caution!)."""
    from .database import engine  # Import here to avoid circular imports

    async with engine.begin() as conn:
        # Drop all tables defined in SQLModel metadata
        await conn.run_sync(SQLModel.metadata.drop_all)