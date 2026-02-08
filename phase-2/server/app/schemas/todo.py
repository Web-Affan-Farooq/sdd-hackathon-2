from pydantic import field_validator
from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime, timezone
from ..models.todo import TodoStatus, TodoBase


class TodoCreate(TodoBase):
    title: str

    @field_validator("user_id", mode="after")
    @classmethod
    def zero_to_none(cls, v: int) -> int:
        """Swagger UI sends 0 for empty nullable int fields."""
        return None if v == 0 else v


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) == 0:
            raise ValueError("Title cannot be empty")
        return v


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def normalize_datetime(cls, v: datetime) -> datetime:
        """Strip timezone for naive UTC database columns."""
        if v and v.tzinfo:
            return v.astimezone(timezone.utc).replace(tzinfo=None)
        return v