from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session


T = TypeVar('T')


class BaseService(ABC, Generic[T]):
    """
    Abstract base service class defining common operations.
    """
    
    @abstractmethod
    def create(self, db: Session, obj: T) -> T:
        """Create a new object in the database."""
        pass
    
    @abstractmethod
    def get(self, db: Session, id: str) -> Optional[T]:
        """Get an object by its ID."""
        pass
    
    @abstractmethod
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with optional pagination."""
        pass
    
    @abstractmethod
    def update(self, db: Session, id: str, obj: T) -> Optional[T]:
        """Update an existing object."""
        pass
    
    @abstractmethod
    def delete(self, db: Session, id: str) -> bool:
        """Delete an object by its ID."""
        pass