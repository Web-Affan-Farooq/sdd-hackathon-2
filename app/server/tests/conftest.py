import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.engine import create_mock_engine
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database.database import engine, get_session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate
from unittest.mock import AsyncMock


@pytest.fixture(scope="function")
def test_client():
    """Create a test client with an in-memory database."""
    # Create an in-memory SQLite database for testing
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(bind=test_engine)

    # Override the get_session dependency
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def mock_user_id():
    """Mock user ID for authentication."""
    return 1