import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.api.main import create_app
from backend.src.config.database import Base, get_db


# Create a test database engine
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db function to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Create the test app
app = create_app()
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_client():
    """Create a test client for the API."""
    with TestClient(app) as client:
        # Create tables
        Base.metadata.create_all(bind=engine)
        yield client
        # Drop tables after tests
        Base.metadata.drop_all(bind=engine)


def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_create_environment(test_client):
    """Test creating a development environment."""
    environment_data = {
        "name": "Test Environment",
        "description": "A test development environment",
        "runtime_version": "Python 3.11",
        "dependencies": {"fastapi": "0.104.1", "sqlalchemy": "2.0.23"},
        "ide_config": {"theme": "dark", "plugins": ["python", "git"]}
    }
    
    response = test_client.post("/v1/environments/", json=environment_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == environment_data["name"]
    assert data["runtime_version"] == environment_data["runtime_version"]
    assert "id" in data
    assert data["id"] is not None


def test_get_environment(test_client):
    """Test retrieving a development environment."""
    # First create an environment
    environment_data = {
        "name": "Get Test Environment",
        "description": "A test environment for GET",
        "runtime_version": "Python 3.11",
        "dependencies": {"fastapi": "0.104.1"},
        "ide_config": {"theme": "light"}
    }
    
    create_response = test_client.post("/v1/environments/", json=environment_data)
    assert create_response.status_code == 201
    created_env = create_response.json()
    
    # Now retrieve it
    env_id = created_env["id"]
    response = test_client.get(f"/v1/environments/{env_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == env_id
    assert data["name"] == environment_data["name"]
    assert data["runtime_version"] == environment_data["runtime_version"]


def test_list_environments(test_client):
    """Test listing development environments."""
    response = test_client.get("/v1/environments/")
    assert response.status_code == 200
    
    data = response.json()
    assert "environments" in data
    assert "pagination" in data
    assert isinstance(data["environments"], list)


def test_update_environment(test_client):
    """Test updating a development environment."""
    # First create an environment
    environment_data = {
        "name": "Update Test Environment",
        "description": "Original description",
        "runtime_version": "Python 3.11",
        "dependencies": {"fastapi": "0.104.1"},
        "ide_config": {"theme": "dark"}
    }
    
    create_response = test_client.post("/v1/environments/", json=environment_data)
    assert create_response.status_code == 201
    created_env = create_response.json()
    
    # Now update it
    env_id = created_env["id"]
    update_data = {
        "name": "Updated Test Environment",
        "description": "Updated description",
        "runtime_version": "Python 3.12"
    }
    
    response = test_client.put(f"/v1/environments/{env_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == env_id
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["runtime_version"] == update_data["runtime_version"]


def test_delete_environment(test_client):
    """Test deleting a development environment."""
    # First create an environment
    environment_data = {
        "name": "Delete Test Environment",
        "description": "An environment to delete",
        "runtime_version": "Python 3.11",
        "dependencies": {"fastapi": "0.104.1"},
        "ide_config": {"theme": "dark"}
    }
    
    create_response = test_client.post("/v1/environments/", json=environment_data)
    assert create_response.status_code == 201
    created_env = create_response.json()
    
    # Now delete it
    env_id = created_env["id"]
    response = test_client.delete(f"/v1/environments/{env_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = test_client.get(f"/v1/environments/{env_id}")
    assert get_response.status_code == 404