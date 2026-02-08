# FastAPI Development Best Practices

This reference outlines the best practices for developing FastAPI applications with SQLModel and PostgreSQL.

## Application Structure

### 1. Application Factory Pattern

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.routes import users, items
from app.config.settings import settings
from app.database.session import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    await create_db_and_tables()
    yield
    # Cleanup on shutdown if needed

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan
    )

    # Include API routes
    app.include_router(users.router, prefix=settings.API_V1_STR)
    app.include_router(items.router, prefix=settings.API_V1_STR)

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the FastAPI backend"}

    return app

app = create_app()
```

### 2. Configuration Management

```python
# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_POOL_RECYCLE: int = 300

    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

## Database Patterns

### 1. Async Session Management

```python
# app/database/session.py
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.database import DATABASE_URL
from collections.abc import AsyncGenerator
from fastapi import Depends

engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
```

### 2. Repository Pattern

```python
# app/repositories/base.py
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func

T = TypeVar('T', bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self._model = model

    async def get(self, session: AsyncSession, id: int) -> Optional[T]:
        statement = select(self._model).where(self._model.id == id)
        result = await session.exec(statement)
        return result.first()

    async def get_multi(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[T]:
        statement = select(self._model).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def create(self, session: AsyncSession, *, obj_in: T) -> T:
        db_obj = self._model.model_validate(obj_in, from_attributes=True)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: T,
        obj_in: Dict[str, Any]
    ) -> T:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, *, id: int) -> T:
        statement = select(self._model).where(self._model.id == id)
        result = await session.exec(statement)
        obj = result.first()

        if not obj:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Object not found")

        await session.delete(obj)
        await session.commit()
        return obj
```

## Error Handling

### 1. Custom Exceptions

```python
# app/exceptions/base.py
from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=self.status_code, detail=detail or self.default_detail)

class UserNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found"

class UserInactiveException(BaseAppException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "User is not active"
```

### 2. Exception Handlers

```python
# app/exceptions/handlers.py
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.exceptions.base import BaseAppException

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def handle_app_exception(request: Request, exc: BaseAppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
```

## Security Considerations

- Always validate and sanitize user inputs
- Use dependency injection for authentication/authorization
- Implement proper rate limiting
- Use HTTPS in production
- Never expose sensitive information in error messages
- Use secure session management
- Implement proper CORS policies
- Use environment variables for sensitive configuration

## Performance Optimization

- Use async/await for I/O-bound operations
- Implement proper database connection pooling
- Use uv for faster package installation and dependency resolution
- Optimize database queries with proper indexing
- Implement caching for expensive operations
- Use background tasks for long-running operations

## Testing Best Practices

- Follow the AAA pattern: Arrange, Act, Assert
- Use parametrized tests for multiple scenarios
- Test both positive and negative cases
- Isolate database tests with proper setup/teardown
- Mock external dependencies in unit tests
- Implement integration tests for API endpoints
- Use fixtures for reusable test components