"""Category repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.category.entities.category import Category


class CategoryRepository(ABC):
    """Abstract repository interface for Category entity."""
    
    @abstractmethod
    async def save(self, category: Category) -> Category:
        """Save a category."""
        pass
    
    @abstractmethod
    async def find_by_id(self, category_id: UUID) -> Optional[Category]:
        """Find category by ID."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Category]:
        """Find category by name."""
        pass
    
    @abstractmethod
    async def find_all(self, enabled_only: bool = False) -> List[Category]:
        """Find all categories."""
        pass

