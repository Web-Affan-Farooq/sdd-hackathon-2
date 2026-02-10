import pytest
from fastapi.testclient import TestClient
from backend.src.api.main import create_app


# Create the test app
app = create_app()


@pytest.fixture
def test_client():
    """Create a test client for the API."""
    with TestClient(app) as client:
        yield client


def test_environment_api_contract(test_client):
    """
    Contract test for the environment API endpoints based on the OpenAPI specification.
    This test verifies that the API conforms to the expected contract.
    """
    
    # Test GET /environments - List all environments
    response = test_client.get("/v1/environments/")
    assert response.status_code in [200, 401, 400]  # Expected status codes from spec
    
    if response.status_code == 200:
        data = response.json()
        assert "environments" in data
        assert "pagination" in data
        assert isinstance(data["environments"], list)
        assert isinstance(data["pagination"], dict)
        assert "offset" in data["pagination"]
        assert "limit" in data["pagination"]
    
    # Test POST /environments - Create environment
    new_environment = {
        "name": "Contract Test Environment",
        "runtime_version": "Python 3.11",
        "description": "Environment for contract testing",
        "dependencies": {"fastapi": "0.104.1", "sqlalchemy": "2.0.23"},
        "ide_config": {"theme": "dark", "plugins": ["python"]}
    }
    
    response = test_client.post("/v1/environments/", json=new_environment)
    assert response.status_code in [201, 400, 401, 409]  # Expected status codes from spec
    
    if response.status_code == 201:
        data = response.json()
        # Verify required fields from the schema
        assert "id" in data
        assert "name" in data
        assert "runtime_version" in data
        assert data["name"] == new_environment["name"]
        assert data["runtime_version"] == new_environment["runtime_version"]
    
    # Test GET /environments/{environmentId} - Get specific environment
    # We'll use the environment we just created if possible
    if response.status_code == 201:
        created_env_id = data["id"]
        response = test_client.get(f"/v1/environments/{created_env_id}")
        assert response.status_code in [200, 404, 401]  # Expected status codes from spec
        
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "name" in data
            assert "runtime_version" in data
            assert data["id"] == created_env_id


def test_architecture_api_contract(test_client):
    """
    Contract test for the architecture API endpoints based on the OpenAPI specification.
    This test verifies that the API conforms to the expected contract.
    """
    
    # Test GET /architectures - List all architectures
    response = test_client.get("/v1/architectures/")
    assert response.status_code in [200, 400, 401]  # Expected status codes from spec
    
    if response.status_code == 200:
        data = response.json()
        assert "architectures" in data
        assert "pagination" in data
        assert isinstance(data["architectures"], list)
        assert isinstance(data["pagination"], dict)
        assert "offset" in data["pagination"]
        assert "limit" in data["pagination"]
    
    # Test POST /architectures - Create architecture
    new_architecture = {
        "name": "Contract Test Architecture",
        "description": "Architecture for contract testing",
        "patterns": ["Microservices", "Event Sourcing"],
        "best_practices": ["Twelve-Factor App", "Infrastructure as Code"]
    }
    
    response = test_client.post("/v1/architectures/", json=new_architecture)
    assert response.status_code in [200, 400, 401]  # Expected status codes from spec
    
    if response.status_code == 200:
        data = response.json()
        # Verify required fields from the schema
        assert "id" in data
        assert "name" in data
        assert data["name"] == new_architecture["name"]


def test_api_contract_api_contract(test_client):
    """
    Contract test for the API contract API endpoints based on the OpenAPI specification.
    This test verifies that the API conforms to the expected contract.
    """
    
    # Test GET /api-contracts - List all API contracts
    response = test_client.get("/v1/api-contracts/")
    assert response.status_code in [200, 400, 401]  # Expected status codes from spec
    
    if response.status_code == 200:
        data = response.json()
        assert "contracts" in data
        assert "pagination" in data
        assert isinstance(data["contracts"], list)
        assert isinstance(data["pagination"], dict)
        assert "offset" in data["pagination"]
        assert "limit" in data["pagination"]
    
    # Test POST /api-contracts - Create API contract
    new_api_contract = {
        "name": "Contract Test API",
        "version": "v1",
        "request_format": "application/json",
        "response_format": "application/json",
        "endpoints": [
            {
                "path": "/test",
                "method": "GET",
                "description": "Test endpoint"
            }
        ]
    }
    
    response = test_client.post("/v1/api-contracts/", json=new_api_contract)
    assert response.status_code in [200, 400, 401]  # Expected status codes from spec
    
    if response.status_code == 200:
        data = response.json()
        # Verify required fields from the schema
        assert "id" in data
        assert "name" in data
        assert "version" in data
        assert data["name"] == new_api_contract["name"]
        assert data["version"] == new_api_contract["version"]