from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ...config.database import get_db
from ...models.api_contract import (
    APIContract,
    APIContractCreate,
    APIContractUpdate
)
from ...services.api_contract_service import APIContractService


router = APIRouter(prefix="", tags=["ApiContracts"])


@router.get("/", response_model=dict)
def list_api_contracts(
    skip: int = Query(0, ge=0, description="Index to start returning results from"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of contracts to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all standardized API contracts.
    """
    service = APIContractService()
    contracts = service.get_all(db, skip=skip, limit=limit)
    
    # Convert SQLAlchemy objects to Pydantic models
    contract_list = []
    for contract in contracts:
        contract_dict = {
            "id": str(contract.id),
            "name": contract.name,
            "version": contract.version,
            "endpoints": contract.endpoints,
            "request_format": contract.request_format,
            "response_format": contract.response_format,
            "error_format": contract.error_format,
            "created_at": contract.created_at.isoformat() if contract.created_at else None,
            "updated_at": contract.updated_at.isoformat() if contract.updated_at else None
        }
        contract_list.append(APIContract(**contract_dict))
    
    return {
        "contracts": contract_list,
        "pagination": {
            "offset": skip,
            "limit": limit,
            "total": len(contract_list)  # In a real implementation, you'd get the actual total count
        }
    }


@router.post("/", response_model=APIContract)
def create_api_contract(
    api_contract: APIContractCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new API contract.
    """
    service = APIContractService()
    
    # Check if API contract with this name and version already exists
    from ...models.api_contract import APIContractDB
    existing_contract = db.query(APIContractDB).filter_by(
        name=api_contract.name, 
        version=api_contract.version
    ).first()
    if existing_contract:
        raise HTTPException(
            status_code=409,  # HTTP_409_CONFLICT
            detail=f"API contract with name '{api_contract.name}' and version '{api_contract.version}' already exists"
        )
    
    created_contract = service.create(db, api_contract)
    # Convert SQLAlchemy object to Pydantic model
    contract_dict = {
        "id": str(created_contract.id),
        "name": created_contract.name,
        "version": created_contract.version,
        "endpoints": created_contract.endpoints,
        "request_format": created_contract.request_format,
        "response_format": created_contract.response_format,
        "error_format": created_contract.error_format,
        "created_at": created_contract.created_at.isoformat() if created_contract.created_at else None,
        "updated_at": created_contract.updated_at.isoformat() if created_contract.updated_at else None
    }
    return APIContract(**contract_dict)


@router.get("/{contract_id}", response_model=APIContract)
def get_api_contract(
    contract_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific API contract.
    """
    service = APIContractService()
    db_contract = service.get(db, contract_id)
    
    if not db_contract:
        raise HTTPException(
            status_code=404,  # HTTP_404_NOT_FOUND
            detail=f"API contract with id '{contract_id}' not found"
        )
    
    # Convert SQLAlchemy object to Pydantic model
    contract_dict = {
        "id": str(db_contract.id),
        "name": db_contract.name,
        "version": db_contract.version,
        "endpoints": db_contract.endpoints,
        "request_format": db_contract.request_format,
        "response_format": db_contract.response_format,
        "error_format": db_contract.error_format,
        "created_at": db_contract.created_at.isoformat() if db_contract.created_at else None,
        "updated_at": db_contract.updated_at.isoformat() if db_contract.updated_at else None
    }
    return APIContract(**contract_dict)