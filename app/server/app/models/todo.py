from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TodoStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TodoStatus = Field(default=TodoStatus.pending)
    user_id: int = Field(index=True)  # For user isolation


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, bread, eggs",
                "status": "pending",
                "user_id": 1
            }
        }