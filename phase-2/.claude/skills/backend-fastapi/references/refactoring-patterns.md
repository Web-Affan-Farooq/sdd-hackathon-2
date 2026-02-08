# FastAPI Refactoring Patterns

This reference provides patterns and strategies for refactoring existing FastAPI applications to improve architecture, maintainability, and performance.

## Code Organization Refactoring

### 1. From Monolithic to Modular Structure

**Before Refactoring:**
```python
# main.py - Everything in one file
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Schemas
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**After Refactoring:**
```python
# app/main.py
from fastapi import FastAPI
from app.api.v1.routes import users
from app.config.settings import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
    )

    app.include_router(users.router, prefix="/api/v1", tags=["users"])

    return app

app = create_app()

# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

# app/api/v1/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Dependency Injection Refactoring

### 2. Improving Dependency Management

**Before Refactoring:**
```python
# Hardcoded dependencies and no separation of concerns
from fastapi import FastAPI, Depends
import redis
import boto3

app = FastAPI()

def get_redis():
    return redis.Redis(host='localhost', port=6379, db=0)

def get_s3_client():
    return boto3.client('s3')

@app.get("/data")
def get_data():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Duplicated
    s3_client = boto3.client('s3')  # Duplicated
    # Business logic here
    return {"data": "result"}
```

**After Refactoring:**
```python
# app/dependencies/cache.py
from typing import Generator
import redis
from app.config.settings import settings

def get_redis_client() -> Generator[redis.Redis, None, None]:
    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )
    try:
        yield client
    finally:
        client.close()

# app/dependencies/storage.py
from typing import Generator
import boto3
from app.config.settings import settings

def get_s3_client() -> Generator[boto3.client, None, None]:
    client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION
    )
    yield client

# app/api/v1/routes/data.py
from fastapi import APIRouter, Depends
import redis
import boto3

router = APIRouter()

@router.get("/data")
def get_data(
    redis_client: redis.Redis = Depends(get_redis_client),
    s3_client: boto3.client = Depends(get_s3_client)
):
    # Business logic using injected dependencies
    cached_data = redis_client.get("key")
    if not cached_data:
        # Fetch from S3 and cache
        s3_client.download_file("bucket", "key", "local_file")
        # Process and cache
        redis_client.setex("key", 3600, "processed_data")
        cached_data = "processed_data"

    return {"data": cached_data}
```

## Error Handling Refactoring

### 3. Centralized Error Handling

**Before Refactoring:**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be positive")

    # Database query
    user = fetch_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Some other validation
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")

    return user
```

**After Refactoring:**
```python
# app/exceptions/base.py
from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=self.status_code, detail=detail or self.default_detail)

class UserNotFoundException(BaseAppException):
    status_code = status_code.HTTP_404_NOT_FOUND
    default_detail = "User not found"

class UserInactiveException(BaseAppException):
    status_code = status_code.HTTP_403_FORBIDDEN
    default_detail = "User is not active"

class InvalidUserIdException(BaseAppException):
    status_code = status_code.HTTP_400_BAD_REQUEST
    default_detail = "User ID must be positive"

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

# app/api/v1/routes/users.py
from fastapi import APIRouter, Depends
from app.exceptions.base import UserNotFoundException, UserInactiveException, InvalidUserIdException

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id <= 0:
        raise InvalidUserIdException()

    user = fetch_user_from_db(user_id)
    if not user:
        raise UserNotFoundException()

    if not user.is_active:
        raise UserInactiveException()

    return user
```

## Database Access Refactoring

### 4. Async Repository Pattern Implementation

**Before Refactoring:**
```python
# Direct synchronous database operations scattered throughout the code
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**After Refactoring:**
```python
# app/repositories/base.py
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlalchemy.orm import selectinload

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

# app/repositories/user.py
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.base import BaseRepository
from sqlmodel import select

class UserRepository(BaseRepository[User]):
    async def get_by_email(self, session: AsyncSession, *, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_active_users(self, session: AsyncSession) -> list[User]:
        statement = select(User).where(User.is_active == True)
        result = await session.exec(statement)
        return result.all()

# Usage in API routes
from app.repositories.user import UserRepository
from app.database.session import get_async_session

@router.post("/", response_model=schemas.UserResponse)
async def create_user(
    user: schemas.UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(User)
    db_user = await user_repo.get_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_repo.create(session=session, obj_in=user)
```

## Configuration Management Refactoring

### 5. Proper Configuration Handling

**Before Refactoring:**
```python
# Hardcoded values and no proper configuration management
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = "postgresql://user:password@localhost/dbname"  # Hardcoded!
SECRET_KEY = "hardcoded-secret-key"  # Security risk!

@app.get("/")
def read_root():
    return {"environment": "development"}  # Environment hardcoded
```

**After Refactoring:**
```python
# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "My API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_TIMEOUT: int = 30

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External services
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # API settings
    API_V1_STR: str = "/api/v1"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# app/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## Testing Refactoring

### 6. Improving Test Structure

**Before Refactoring:**
```python
# tests/test_main.py - Poor test organization
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "name": "John Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 200

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
```

**After Refactoring:**
```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.base import Base
from app.database.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_db_override():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()

# tests/api/v1/test_users.py
import pytest
from httpx import AsyncClient

class TestUserAPI:
    @pytest.mark.asyncio
    async def test_create_user_success(self, client: AsyncClient):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, client: AsyncClient):
        # First create a user
        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        await client.post("/api/v1/users/", json=user_data)

        # Try to create another user with same email
        duplicate_data = {
            "name": "Jane Doe",
            "email": "john@example.com"
        }
        response = await client.post("/api/v1/users/", json=duplicate_data)
        assert response.status_code == 400
```

## Refactoring Checklist

- [ ] Move from monolithic to modular structure
- [ ] Separate concerns (models, schemas, API routes, business logic)
- [ ] Implement proper dependency injection
- [ ] Create centralized error handling
- [ ] Apply repository pattern for database access
- [ ] Improve configuration management
- [ ] Enhance test structure and coverage
- [ ] Add proper logging
- [ ] Implement caching strategies
- [ ] Add security measures
- [ ] Optimize database queries
- [ ] Add proper documentation