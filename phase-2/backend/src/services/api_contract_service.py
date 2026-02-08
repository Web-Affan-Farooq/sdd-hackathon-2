from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.api_contract import APIContractDB, APIContractCreate, APIContractUpdate
from ..services import BaseService


class APIContractService(BaseService[APIContractDB]):
    """
    Service for managing API contracts.
    """
    
    def create(self, db: Session, obj: APIContractCreate) -> APIContractDB:
        """Create a new API contract."""
        db_obj = APIContractDB(
            name=obj.name,
            version=obj.version,
            endpoints=obj.endpoints,
            request_format=obj.request_format,
            response_format=obj.response_format,
            error_format=obj.error_format
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: str) -> Optional[APIContractDB]:
        """Get an API contract by its ID."""
        return db.query(APIContractDB).filter(APIContractDB.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[APIContractDB]:
        """Get all API contracts with optional pagination."""
        return db.query(APIContractDB).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: str, obj: APIContractUpdate) -> Optional[APIContractDB]:
        """Update an existing API contract."""
        db_obj = self.get(db, id)
        if db_obj:
            update_data = obj.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: str) -> bool:
        """Delete an API contract by its ID."""
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False