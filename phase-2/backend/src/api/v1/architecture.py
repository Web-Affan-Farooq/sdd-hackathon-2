from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ...config.database import get_db
from ...models.service_architecture import (
    ServiceArchitecture,
    ServiceArchitectureCreate,
    ServiceArchitectureUpdate
)
from ...services.architecture_validation import ArchitectureValidationService


router = APIRouter(prefix="", tags=["Architectures"])


@router.get("/", response_model=dict)
def list_architectures(
    skip: int = Query(0, ge=0, description="Index to start returning results from"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of architectures to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all available service architecture patterns.
    """
    service = ArchitectureValidationService()
    architectures = service.get_all(db, skip=skip, limit=limit)
    
    # Convert SQLAlchemy objects to Pydantic models
    architecture_list = []
    for arch in architectures:
        arch_dict = {
            "id": str(arch.id),
            "name": arch.name,
            "description": arch.description,
            "patterns": arch.patterns,
            "best_practices": arch.best_practices,
            "created_at": arch.created_at.isoformat() if arch.created_at else None,
            "updated_at": arch.updated_at.isoformat() if arch.updated_at else None
        }
        architecture_list.append(ServiceArchitecture(**arch_dict))
    
    return {
        "architectures": architecture_list,
        "pagination": {
            "offset": skip,
            "limit": limit,
            "total": len(architecture_list)  # In a real implementation, you'd get the actual total count
        }
    }


@router.post("/", response_model=ServiceArchitecture)
def create_architecture(
    architecture: ServiceArchitectureCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new service architecture pattern.
    """
    service = ArchitectureValidationService()
    
    # Check if architecture with this name already exists
    from ...models.service_architecture import ServiceArchitectureDB
    existing_arch = db.query(ServiceArchitectureDB).filter_by(name=architecture.name).first()
    if existing_arch:
        raise HTTPException(
            status_code=409,  # HTTP_409_CONFLICT
            detail=f"Architecture with name '{architecture.name}' already exists"
        )
    
    created_arch = service.create(db, architecture)
    # Convert SQLAlchemy object to Pydantic model
    arch_dict = {
        "id": str(created_arch.id),
        "name": created_arch.name,
        "description": created_arch.description,
        "patterns": created_arch.patterns,
        "best_practices": created_arch.best_practices,
        "created_at": created_arch.created_at.isoformat() if created_arch.created_at else None,
        "updated_at": created_arch.updated_at.isoformat() if created_arch.updated_at else None
    }
    return ServiceArchitecture(**arch_dict)


@router.get("/{architecture_id}", response_model=ServiceArchitecture)
def get_architecture(
    architecture_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific service architecture.
    """
    service = ArchitectureValidationService()
    db_architecture = service.get(db, architecture_id)
    
    if not db_architecture:
        raise HTTPException(
            status_code=404,  # HTTP_404_NOT_FOUND
            detail=f"Service architecture with id '{architecture_id}' not found"
        )
    
    # Convert SQLAlchemy object to Pydantic model
    arch_dict = {
        "id": str(db_architecture.id),
        "name": db_architecture.name,
        "description": db_architecture.description,
        "patterns": db_architecture.patterns,
        "best_practices": db_architecture.best_practices,
        "created_at": db_architecture.created_at.isoformat() if db_architecture.created_at else None,
        "updated_at": db_architecture.updated_at.isoformat() if db_architecture.updated_at else None
    }
    return ServiceArchitecture(**arch_dict)