from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import settings


# Create the database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create a SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create a Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()