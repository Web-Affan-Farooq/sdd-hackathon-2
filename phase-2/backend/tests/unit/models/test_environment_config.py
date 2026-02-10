import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.src.models.environment_config import DevelopmentEnvironmentDB


@pytest.fixture
def db_session():
    """Create a test database session."""
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", echo=True)
    
    # Create tables
    from backend.src.config.database import Base
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    # Close the session
    session.close()


def test_development_environment_creation(db_session):
    """Test creating a DevelopmentEnvironment object."""
    # Create a DevelopmentEnvironment object
    dev_env = DevelopmentEnvironmentDB(
        name="Test Environment",
        description="A test development environment",
        runtime_version="Python 3.11",
        dependencies={"fastapi": "0.104.1", "sqlalchemy": "2.0.23"},
        ide_config={"theme": "dark", "plugins": ["python", "git"]}
    )
    
    # Add to session and commit
    db_session.add(dev_env)
    db_session.commit()
    db_session.refresh(dev_env)
    
    # Assertions
    assert dev_env.id is not None
    assert dev_env.name == "Test Environment"
    assert dev_env.description == "A test development environment"
    assert dev_env.runtime_version == "Python 3.11"
    assert dev_env.dependencies is not None
    assert dev_env.ide_config is not None
    assert dev_env.created_at is not None
    assert dev_env.updated_at is not None


def test_development_environment_defaults(db_session):
    """Test DevelopmentEnvironment with minimal required fields."""
    dev_env = DevelopmentEnvironmentDB(
        name="Minimal Env",
        runtime_version="Python 3.11"
    )
    
    db_session.add(dev_env)
    db_session.commit()
    db_session.refresh(dev_env)
    
    # Assertions
    assert dev_env.id is not None
    assert dev_env.name == "Minimal Env"
    assert dev_env.runtime_version == "Python 3.11"
    # Optional fields should be None or have default values
    assert dev_env.description is None
    assert dev_env.dependencies is None
    assert dev_env.ide_config is None
    assert dev_env.created_at is not None
    assert dev_env.updated_at is not None