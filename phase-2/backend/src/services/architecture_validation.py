from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.service_architecture import ServiceArchitectureDB, ServiceArchitectureCreate, ServiceArchitectureUpdate
from ..services import BaseService


class ArchitectureValidationService(BaseService[ServiceArchitectureDB]):
    """
    Service for managing service architectures.
    """
    
    def create(self, db: Session, obj: ServiceArchitectureCreate) -> ServiceArchitectureDB:
        """Create a new service architecture."""
        db_obj = ServiceArchitectureDB(
            name=obj.name,
            description=obj.description,
            patterns=obj.patterns,
            best_practices=obj.best_practices
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: str) -> Optional[ServiceArchitectureDB]:
        """Get a service architecture by its ID."""
        return db.query(ServiceArchitectureDB).filter(ServiceArchitectureDB.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ServiceArchitectureDB]:
        """Get all service architectures with optional pagination."""
        return db.query(ServiceArchitectureDB).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: str, obj: ServiceArchitectureUpdate) -> Optional[ServiceArchitectureDB]:
        """Update an existing service architecture."""
        db_obj = self.get(db, id)
        if db_obj:
            update_data = obj.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: str) -> bool:
        """Delete a service architecture by its ID."""
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False