# FastAPI Testing Patterns

This reference covers comprehensive testing strategies for FastAPI applications.

## Testing Setup

### Basic Test Configuration

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database.base import Base
from app.database.session import get_async_session
from collections.abc import AsyncGenerator

# Test database setup - using in-memory SQLite for tests or separate test PostgreSQL
TEST_DATABASE_URL = "postgresql+asyncpg://testuser:testpassword@localhost:5432/testdb"

# For local testing without PostgreSQL, you can use SQLite with async support:
# TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    # For SQLite testing only:
    # connect_args={"check_same_thread": False},
    # poolclass=StaticPool,  # For SQLite
)

@pytest.fixture(scope="module")
async def create_test_database():
    """Create test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def async_session(create_test_database) -> AsyncGenerator[AsyncSession, None]:
    """Create a clean database session for each test."""
    async with AsyncSession(test_engine) as session:
        yield session

@pytest.fixture
async def client(async_session):
    """Create test client with database overrides."""

    async def override_get_async_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()
```

## API Endpoint Testing

### Testing GET Requests

```python
# tests/api/test_users.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_users(client: AsyncClient):
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_read_user_by_id(client: AsyncClient):
    response = await client.get("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "username" in data
```

### Testing POST Requests

```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
```

### Testing PUT/PATCH Requests

```python
@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    update_data = {
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = await client.put("/api/v1/users/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
```

### Testing DELETE Requests

```python
@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    response = await client.delete("/api/v1/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["deleted"] is True
```

## Security and Authentication Testing

### Testing Protected Endpoints

```python
@pytest.mark.asyncio
async def test_protected_endpoint_without_auth(client: AsyncClient):
    response = await client.get("/api/v1/protected/")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_with_auth(client: AsyncClient):
    # Assuming you have a way to obtain a valid token
    headers = {"Authorization": "Bearer valid_jwt_token"}
    response = await client.get("/api/v1/protected/", headers=headers)
    assert response.status_code == 200
```

## Database Testing

### Testing Database Operations

```python
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.users import create_user, get_user_by_id

@pytest.mark.asyncio
async def test_database_operations(test_db):
    # Test creating a user
    user_create = UserCreate(
        username="testuser",
        email="test@example.com",
        password="hashed_password"
    )
    created_user = create_user(test_db, user_create)
    assert created_user.username == "testuser"
    assert created_user.email == "test@example.com"

    # Test retrieving the user
    retrieved_user = get_user_by_id(test_db, created_user.id)
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == created_user.username
```

## Validation Testing

### Testing Request Validation

```python
@pytest.mark.asyncio
async def test_invalid_request_validation(client: AsyncClient):
    invalid_data = {
        "invalid_field": "some_value",  # Field not in schema
        "missing_required": None  # Missing required field
    }
    response = await client.post("/api/v1/users/", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_field_validation(client: AsyncClient):
    invalid_data = {
        "username": "",  # Empty username (should be invalid)
        "email": "invalid-email",  # Invalid email format
        "password": "short"  # Password too short
    }
    response = await client.post("/api/v1/users/", json=invalid_data)
    assert response.status_code == 422
```

## Error Handling Testing

### Testing Custom Exception Handlers

```python
@pytest.mark.asyncio
async def test_custom_exception_handling(client: AsyncClient):
    # Simulate an internal server error
    response = await client.get("/api/v1/error-test/")
    assert response.status_code == 500
    error_data = response.json()
    assert "detail" in error_data
```

## Background Tasks Testing

### Testing Background Task Execution

```python
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_background_task_execution(client: AsyncClient):
    with patch('app.tasks.send_notification') as mock_task:
        response = await client.post("/api/v1/send-notification/", json={
            "message": "Test notification"
        })
        assert response.status_code == 200

        # Verify the background task was scheduled
        assert mock_task.called
```

## Testing with Different Scenarios

### Parametrized Tests

```python
import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize("username,email", [
    ("user1", "user1@example.com"),
    ("user2", "user2@example.com"),
    ("testuser", "test@example.com"),
])
async def test_multiple_users_creation(client: AsyncClient, username: str, email: str):
    user_data = {
        "username": username,
        "email": email,
        "password": "securepassword"
    }
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email
```

## Performance Testing

### Basic Performance Test

```python
import time

@pytest.mark.performance
@pytest.mark.asyncio
async def test_endpoint_performance(client: AsyncClient):
    start_time = time.time()

    # Make multiple requests
    for _ in range(100):
        response = await client.get("/api/v1/users/")
        assert response.status_code == 200

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Assert that 100 requests took less than 5 seconds
    assert elapsed_time < 5.0
```

## Testing Utilities

### Test Data Factory

```python
from app.schemas.user import UserCreate
from faker import Faker

fake = Faker()

def create_test_user_data() -> dict:
    """Create randomized test user data."""
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password()
    }

def create_test_user_schema() -> UserCreate:
    """Create a test user schema."""
    data = create_test_user_data()
    return UserCreate(**data)
```

## Testing Checklist

- [ ] All API endpoints have test coverage
- [ ] Positive and negative test cases are included
- [ ] Database operations are tested in isolation
- [ ] Authentication and authorization are tested
- [ ] Request validation is thoroughly tested
- [ ] Error handling scenarios are covered
- [ ] Background tasks are tested appropriately
- [ ] Security aspects are tested
- [ ] Edge cases are considered
- [ ] Performance tests are included for critical paths