# Async CRUD Operations with SQLModel

This reference covers the async CRUD operations patterns for FastAPI applications using SQLModel and PostgreSQL.

## Async Base Repository Pattern

```python
# app/repositories/base.py
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlmodel import SQLModel, select, Session, Field
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

T = TypeVar('T', bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self._model = model

    async def get(self, session: AsyncSession, id: int) -> Optional[T]:
        """Get a record by ID."""
        statement = select(self._model).where(self._model.id == id)
        result = await session.exec(statement)
        return result.first()

    async def get_multi(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """Get multiple records with pagination and optional filters."""
        statement = select(self._model)

        if filters:
            for field, value in filters.items():
                column = getattr(self._model, field)
                statement = statement.where(column == value)

        statement = statement.offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def create(self, session: AsyncSession, *, obj_in: T) -> T:
        """Create a new record."""
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
        """Update an existing record."""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, *, id: int) -> T:
        """Remove a record by ID."""
        statement = select(self._model).where(self._model.id == id)
        result = await session.exec(statement)
        obj = result.first()

        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self._model.__name__} not found"
            )

        await session.delete(obj)
        await session.commit()
        return obj

    async def count(self, session: AsyncSession) -> int:
        """Count all records."""
        statement = select(func.count(self._model.id))
        result = await session.exec(statement)
        return result.one()
```

## Async User Repository Example

```python
# app/repositories/user.py
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.repositories.base import BaseRepository
from fastapi import HTTPException

class UserRepository(BaseRepository[User]):
    async def get_by_email(self, session: AsyncSession, *, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_by_username(self, session: AsyncSession, *, username: str) -> Optional[User]:
        """Get user by username."""
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()

    async def get_active_users(self, session: AsyncSession) -> list[User]:
        """Get all active users."""
        statement = select(User).where(User.is_active == True)
        result = await session.exec(statement)
        return result.all()

    async def create(self, session: AsyncSession, *, obj_in: User) -> User:
        """Create user with validation."""
        # Check if user with same email already exists
        existing_user = await self.get_by_email(session, email=obj_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Check if user with same username already exists
        existing_username = await self.get_by_username(session, username=obj_in.username)
        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

        return await super().create(session=session, obj_in=obj_in)
```

## Usage in API Routes

```python
# app/api/v1/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.session import get_async_session
from app.schemas.user import UserCreate, User
from app.repositories.user import UserRepository
from typing import List

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new user."""
    user_repo = UserRepository(User)
    try:
        user = await user_repo.create(session=session, obj_in=user_in)
        return user
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific user by ID."""
    user_repo = UserRepository(User)
    user = await user_repo.get(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    """Get users with pagination."""
    user_repo = UserRepository(User)
    users = await user_repo.get_multi(session, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Update a user."""
    user_repo = UserRepository(User)
    user = await user_repo.get(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert schema to dict for update
    update_data = user_in.model_dump(exclude_unset=True)
    updated_user = await user_repo.update(session, db_obj=user, obj_in=update_data)
    return updated_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a user."""
    user_repo = UserRepository(User)
    try:
        await user_repo.remove(session, id=user_id)
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete user: {str(e)}"
        )
```

## Advanced Querying with Relationships

```python
# Enhanced repository with relationship loading
class UserRepository(BaseRepository[User]):
    async def get_user_with_items(
        self,
        session: AsyncSession,
        *,
        user_id: int
    ) -> Optional[User]:
        """Get user with their associated items."""
        statement = (
            select(User)
            .options(selectinload(User.items))
            .where(User.id == user_id)
        )
        result = await session.exec(statement)
        return result.first()

    async def get_users_with_items(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get users with their associated items."""
        statement = (
            select(User)
            .options(selectinload(User.items))
            .offset(skip)
            .limit(limit)
        )
        result = await session.exec(statement)
        return result.unique().all()  # unique() required with selectinload
```

## Error Handling Patterns

```python
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException

async def create_user_safe(
    session: AsyncSession,
    user_in: UserCreate
) -> User:
    """Create user with comprehensive error handling."""
    try:
        user_repo = UserRepository(User)
        user = await user_repo.create(session=session, obj_in=user_in)
        return user
    except IntegrityError as e:
        await session.rollback()
        if "users_email_key" in str(e) or "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists"
            )
        elif "users_username_key" in str(e):
            raise HTTPException(
                status_code=400,
                detail="A user with this username already exists"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Database integrity error occurred"
            )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
```

## Bulk Operations

```python
class BaseRepository(Generic[T]):
    async def create_many(
        self,
        session: AsyncSession,
        *,
        objs_in: List[T]
    ) -> List[T]:
        """Create multiple records in a single transaction."""
        db_objs = []
        for obj_in in objs_in:
            db_obj = self._model.model_validate(obj_in, from_attributes=True)
            db_objs.append(db_obj)

        session.add_all(db_objs)
        await session.commit()

        # Refresh all objects to get their IDs
        for db_obj in db_objs:
            await session.refresh(db_obj)

        return db_objs

    async def update_many(
        self,
        session: AsyncSession,
        *,
        updates: List[Dict[str, Any]]
    ) -> List[T]:
        """Update multiple records."""
        updated_objs = []
        for update_data in updates:
            obj_id = update_data.pop('id', None)
            if obj_id:
                obj = await self.get(session, obj_id)
                if obj:
                    updated_obj = await self.update(
                        session,
                        db_obj=obj,
                        obj_in=update_data
                    )
                    updated_objs.append(updated_obj)

        return updated_objs
```