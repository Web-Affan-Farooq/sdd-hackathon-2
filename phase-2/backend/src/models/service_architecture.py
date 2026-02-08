from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from ..models import BaseMixin
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid


class ServiceArchitectureDB(BaseMixin):
    """
    SQLAlchemy model for ServiceArchitecture entity.
    """
    __tablename__ = "service_architectures"

    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    patterns = Column(JSONB, nullable=True)  # JSON field for architectural patterns
    best_practices = Column(JSONB, nullable=True)  # JSON field for best practices


# Pydantic models for API
class ServiceArchitectureBase(BaseModel):
    name: str
    description: Optional[str] = None
    patterns: Optional[List[str]] = None
    best_practices: Optional[List[str]] = None


class ServiceArchitectureCreate(ServiceArchitectureBase):
    pass


class ServiceArchitectureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    patterns: Optional[List[str]] = None
    best_practices: Optional[List[str]] = None


class ServiceArchitecture(ServiceArchitectureBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True