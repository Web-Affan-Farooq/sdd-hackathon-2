from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from ..models import BaseMixin
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid


class DevelopmentEnvironmentDB(BaseMixin):
    """
    SQLAlchemy model for DevelopmentEnvironment entity.
    """
    __tablename__ = "development_environments"

    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    runtime_version = Column(String, nullable=False)
    dependencies = Column(JSONB, nullable=True)  # JSON field for dependencies
    ide_config = Column(JSONB, nullable=True)   # JSON field for IDE configuration


class EnvironmentConfigDB(BaseMixin):
    """
    SQLAlchemy model for EnvironmentConfig entity.
    """
    __tablename__ = "environment_configs"

    environment_type = Column(String, nullable=False)  # development, staging, production
    config_params = Column(JSONB, nullable=True)       # JSON field for configuration parameters
    encrypted_secrets = Column(JSONB, nullable=True)   # JSON field for encrypted secrets


# Pydantic models for API
class DevelopmentEnvironmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    runtime_version: str
    dependencies: Optional[Dict[str, Any]] = None
    ide_config: Optional[Dict[str, Any]] = None


class DevelopmentEnvironmentCreate(DevelopmentEnvironmentBase):
    pass


class DevelopmentEnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    runtime_version: Optional[str] = None
    dependencies: Optional[Dict[str, Any]] = None
    ide_config: Optional[Dict[str, Any]] = None


class DevelopmentEnvironment(DevelopmentEnvironmentBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class EnvironmentConfigBase(BaseModel):
    environment_type: str
    config_params: Optional[Dict[str, Any]] = None
    encrypted_secrets: Optional[Dict[str, Any]] = None


class EnvironmentConfigCreate(EnvironmentConfigBase):
    pass


class EnvironmentConfigUpdate(BaseModel):
    environment_type: Optional[str] = None
    config_params: Optional[Dict[str, Any]] = None
    encrypted_secrets: Optional[Dict[str, Any]] = None


class EnvironmentConfig(EnvironmentConfigBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True