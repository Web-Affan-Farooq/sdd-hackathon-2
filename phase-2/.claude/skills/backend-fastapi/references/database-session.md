# Database Session Management

This reference covers the async database session management patterns for FastAPI applications using SQLModel and PostgreSQL.

## Async Session Dependency

```python
# app/database/session.py
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.database import engine
from collections.abc import AsyncGenerator
from fastapi import Depends

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields async database sessions."""
    async with AsyncSession(engine) as session:
        yield session

# Usage in API routes
from fastapi import Depends
from app.database.session import get_async_session

@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Session Management Best Practices

### 1. Proper Error Handling with Sessions

```python
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

async def create_user_safe(
    session: AsyncSession,
    user_data: UserCreate
) -> User:
    try:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.hashed_password
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )
```

### 2. Transaction Management

```python
# For complex operations requiring transactions
async def complex_user_operation(
    session: AsyncSession,
    user_id: int
) -> bool:
    try:
        # Get user
        user = await session.get(User, user_id)
        if not user:
            return False

        # Perform multiple operations
        user.last_login = datetime.utcnow()

        # Add audit log
        audit_log = AuditLog(
            user_id=user_id,
            action="login",
            timestamp=datetime.utcnow()
        )
        session.add(audit_log)

        await session.commit()
        return True
    except Exception:
        await session.rollback()
        raise
```

### 3. Using selectinload for Relationships

```python
from sqlalchemy.orm import selectinload
from sqlmodel import select

async def get_user_with_items(
    session: AsyncSession,
    user_id: int
) -> User | None:
    statement = (
        select(User)
        .options(selectinload(User.items))
        .where(User.id == user_id)
    )
    result = await session.exec(statement)
    return result.first()
```

## Testing with Async Sessions

### 1. Test Session Override

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config.database import DATABASE_URL
from app.main import app
from app.database.session import get_async_session

@pytest.fixture
async def async_client():
    # Create test engine
    test_engine = create_async_engine(DATABASE_URL.replace("dbname=", "dbname=test_"))

    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Override dependency
    async def override_get_async_session():
        async with AsyncSession(test_engine) as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
```

### 2. Session Fixture for Direct Database Access

```python
# tests/conftest.py
@pytest.fixture
async def db_session(async_client):
    # This gives direct access to the session for setup/cleanup
    async with AsyncSession(create_async_engine(DATABASE_URL)) as session:
        yield session
```

## Connection Pool Configuration

```python
# Best practices for connection pools in production
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,                    # Number of connection objects to maintain
    max_overflow=20,                 # Additional connections beyond pool_size
    pool_pre_ping=True,              # Verify connections before use (essential for cloud DBs)
    pool_recycle=300,                # Recycle connections after 5 minutes
    pool_timeout=30,                 # Seconds to wait before giving up on getting a connection
    echo=False                       # Set to True for SQL query logging
)
```

## Health Checks

```python
# Add database health check endpoint
from fastapi import HTTPException
import asyncio

@router.get("/health/db")
async def check_db_health(
    session: AsyncSession = Depends(get_async_session)
):
    try:
        # Simple query to test connection
        await session.exec("SELECT 1")
        return {"status": "healthy", "database": "reachable"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {str(e)}"
        )
```