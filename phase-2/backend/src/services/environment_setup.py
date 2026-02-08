from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.environment_config import DevelopmentEnvironmentDB, DevelopmentEnvironmentCreate, DevelopmentEnvironmentUpdate
from ..services import BaseService


class EnvironmentSetupService(BaseService[DevelopmentEnvironmentDB]):
    """
    Service for managing development environments.
    """
    
    def create(self, db: Session, obj: DevelopmentEnvironmentCreate) -> DevelopmentEnvironmentDB:
        """Create a new development environment."""
        db_obj = DevelopmentEnvironmentDB(
            name=obj.name,
            description=obj.description,
            runtime_version=obj.runtime_version,
            dependencies=obj.dependencies,
            ide_config=obj.ide_config
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: str) -> Optional[DevelopmentEnvironmentDB]:
        """Get a development environment by its ID."""
        return db.query(DevelopmentEnvironmentDB).filter(DevelopmentEnvironmentDB.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[DevelopmentEnvironmentDB]:
        """Get all development environments with optional pagination."""
        return db.query(DevelopmentEnvironmentDB).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: str, obj: DevelopmentEnvironmentUpdate) -> Optional[DevelopmentEnvironmentDB]:
        """Update an existing development environment."""
        db_obj = self.get(db, id)
        if db_obj:
            update_data = obj.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: str) -> bool:
        """Delete a development environment by its ID."""
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False