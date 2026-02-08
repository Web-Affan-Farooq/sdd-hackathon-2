from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from ..models import BaseMixin
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid


class APIContractDB(BaseMixin):
    """
    SQLAlchemy model for APIContract entity.
    """
    __tablename__ = "api_contracts"

    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    endpoints = Column(JSONB, nullable=True)  # JSON field for API endpoints
    request_format = Column(String, nullable=True)  # e.g., "application/json"
    response_format = Column(String, nullable=True)  # e.g., "application/json"
    error_format = Column(JSONB, nullable=True)  # JSON field for standard error format

    __table_args__ = (
        # Ensure name and version combination is unique
        {'sqlite_autoincrement': True}
    )


# Pydantic models for API
class EndpointBase(BaseModel):
    path: str
    method: str
    description: str
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None


class APIContractBase(BaseModel):
    name: str
    version: str
    endpoints: Optional[List[EndpointBase]] = None
    request_format: Optional[str] = "application/json"
    response_format: Optional[str] = "application/json"
    error_format: Optional[Dict[str, Any]] = None


class APIContractCreate(APIContractBase):
    pass


class APIContractUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    endpoints: Optional[List[EndpointBase]] = None
    request_format: Optional[str] = None
    response_format: Optional[str] = None
    error_format: Optional[Dict[str, Any]] = None


class APIContract(APIContractBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True