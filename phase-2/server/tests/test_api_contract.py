import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.todo import TodoStatus
import json


def test_api_contract_compliance():
    """Test that API endpoints match the specified contract."""
    client = TestClient(app)

    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    # Test todos endpoints exist (without authentication, should return 401/403)
    response = client.get("/todos/")
    assert response.status_code in [401, 403]  # Should require authentication

    response = client.post("/todos/", json={"title": "test", "user_id": 1})
    assert response.status_code in [401, 403]  # Should require authentication

    response = client.get("/todos/1")
    assert response.status_code in [401, 403]  # Should require authentication

    response = client.put("/todos/1", json={})
    assert response.status_code in [401, 403]  # Should require authentication

    response = client.delete("/todos/1")
    assert response.status_code in [401, 403]  # Should require authentication


def test_request_response_schemas():
    """Test that request/response schemas match specifications."""
    # This test would normally validate against an OpenAPI spec
    # Here we're checking basic compliance

    # Check that the OpenAPI schema is available
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()

    # Check that all expected endpoints are documented
    paths = openapi_spec.get("paths", {})
    expected_paths = ["/todos/", "/todos/{todo_id}"]

    for path in expected_paths:
        assert path in paths, f"Path {path} not found in OpenAPI spec"

    # Check that the expected methods are available
    todos_path = paths.get("/todos/", {})
    assert "get" in todos_path, "GET /todos/ not in OpenAPI spec"
    assert "post" in todos_path, "POST /todos/ not in OpenAPI spec"


def test_status_codes():
    """Test that endpoints return expected status codes."""
    client = TestClient(app)

    # Without authentication, we expect 401/403
    response = client.get("/todos/")
    assert response.status_code in [401, 403]

    response = client.post("/todos/", json={"title": "test", "user_id": 1})
    assert response.status_code in [401, 403]

    response = client.get("/todos/1")
    assert response.status_code in [401, 403]

    response = client.put("/todos/1", json={})
    assert response.status_code in [401, 403]

    response = client.delete("/todos/1")
    assert response.status_code in [401, 403]


def test_error_responses():
    """Test that error responses match specification."""
    client = TestClient(app)

    # Test that unauthorized requests return proper error format
    response = client.get("/todos/")
    if response.status_code == 401:
        # Check for expected error response structure
        error_response = response.json()
        assert "detail" in error_response  # Standard FastAPI error format