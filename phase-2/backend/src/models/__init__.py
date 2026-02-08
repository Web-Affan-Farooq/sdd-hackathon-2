from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from pydantic import BaseModel, Field
from typing import Optional
import uuid


class BaseMixin:
    """
    Base mixin to add common columns to all models.
    """
    id = Column('id', 'UUID', primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class BasePydanticModel(BaseModel):
    """
    Base Pydantic model with common configurations.
    """
    id: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True