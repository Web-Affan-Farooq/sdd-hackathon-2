from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...config.database import get_db
from ...models.environment_config import (
    DevelopmentEnvironment,
    DevelopmentEnvironmentCreate,
    DevelopmentEnvironmentUpdate,
    EnvironmentConfig,
    EnvironmentConfigCreate,
    EnvironmentConfigUpdate
)
from ...services.environment_setup import EnvironmentSetupService


router = APIRouter(prefix="", tags=["Environments"])


@router.get("/", response_model=dict)
def list_environments(
    skip: int = Query(0, ge=0, description="Index to start returning results from"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of environments to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all available development environments.
    """
    service = EnvironmentSetupService()
    environments = service.get_all(db, skip=skip, limit=limit)
    
    # Convert SQLAlchemy objects to Pydantic models
    environment_list = []
    for env in environments:
        env_dict = {
            "id": str(env.id),
            "name": env.name,
            "description": env.description,
            "runtime_version": env.runtime_version,
            "dependencies": env.dependencies,
            "ide_config": env.ide_config,
            "created_at": env.created_at.isoformat() if env.created_at else None,
            "updated_at": env.updated_at.isoformat() if env.updated_at else None
        }
        environment_list.append(DevelopmentEnvironment(**env_dict))
    
    return {
        "environments": environment_list,
        "pagination": {
            "offset": skip,
            "limit": limit,
            "total": len(environment_list)  # In a real implementation, you'd get the actual total count
        }
    }


@router.post("/", response_model=DevelopmentEnvironment, status_code=status.HTTP_201_CREATED)
def create_environment(
    environment: DevelopmentEnvironmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new standardized development environment configuration.
    """
    service = EnvironmentSetupService()
    
    # Check if environment with this name already exists
    from ...models.environment_config import DevelopmentEnvironmentDB
    existing_env = db.query(DevelopmentEnvironmentDB).filter_by(name=environment.name).first()
    if existing_env:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Environment with name '{environment.name}' already exists"
        )
    
    created_env = service.create(db, environment)
    # Convert SQLAlchemy object to Pydantic model
    env_dict = {
        "id": str(created_env.id),
        "name": created_env.name,
        "description": created_env.description,
        "runtime_version": created_env.runtime_version,
        "dependencies": created_env.dependencies,
        "ide_config": created_env.ide_config,
        "created_at": created_env.created_at.isoformat() if created_env.created_at else None,
        "updated_at": created_env.updated_at.isoformat() if created_env.updated_at else None
    }
    return DevelopmentEnvironment(**env_dict)


@router.get("/{environment_id}", response_model=DevelopmentEnvironment)
def get_environment(
    environment_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific development environment.
    """
    service = EnvironmentSetupService()
    db_environment = service.get(db, environment_id)
    
    if not db_environment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Development environment with id '{environment_id}' not found"
        )
    
    # Convert SQLAlchemy object to Pydantic model
    env_dict = {
        "id": str(db_environment.id),
        "name": db_environment.name,
        "description": db_environment.description,
        "runtime_version": db_environment.runtime_version,
        "dependencies": db_environment.dependencies,
        "ide_config": db_environment.ide_config,
        "created_at": db_environment.created_at.isoformat() if db_environment.created_at else None,
        "updated_at": db_environment.updated_at.isoformat() if db_environment.updated_at else None
    }
    return DevelopmentEnvironment(**env_dict)


@router.put("/{environment_id}", response_model=DevelopmentEnvironment)
def update_environment(
    environment_id: str,
    environment_update: DevelopmentEnvironmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the configuration of an existing development environment.
    """
    service = EnvironmentSetupService()
    updated_env = service.update(db, environment_id, environment_update)
    
    if not updated_env:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Development environment with id '{environment_id}' not found"
        )
    
    # Convert SQLAlchemy object to Pydantic model
    env_dict = {
        "id": str(updated_env.id),
        "name": updated_env.name,
        "description": updated_env.description,
        "runtime_version": updated_env.runtime_version,
        "dependencies": updated_env.dependencies,
        "ide_config": updated_env.ide_config,
        "created_at": updated_env.created_at.isoformat() if updated_env.created_at else None,
        "updated_at": updated_env.updated_at.isoformat() if updated_env.updated_at else None
    }
    return DevelopmentEnvironment(**env_dict)


@router.delete("/{environment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_environment(
    environment_id: str,
    db: Session = Depends(get_db)
):
    """
    Remove a development environment configuration.
    """
    service = EnvironmentSetupService()
    success = service.delete(db, environment_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Development environment with id '{environment_id}' not found"
        )
    
    return