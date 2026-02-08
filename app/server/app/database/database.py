from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from typing import AsyncGenerator
from ..config.settings import settings


def get_async_database_url(url: str) -> str:
    """Convert postgresql:// to postgresql+asyncpg://"""
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


DATABASE_URL = get_async_database_url(settings.database_url)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,    # Essential for managed DBs (Neon, Supabase)
    pool_recycle=300,      # Recycle connections every 5 minutes
)


async def create_db_and_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[SQLModelAsyncSession, None]:
    """Dependency that yields async database sessions."""
    async with SQLModelAsyncSession(engine) as session:
        yield session