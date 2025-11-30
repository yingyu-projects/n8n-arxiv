"""Category repository implementation for PostgreSQL."""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.category.repositories.category_repository import CategoryRepository
from app.domain.category.entities.category import Category
from app.infrastructure.database.models.category_orm import CategoryORM
from app.infrastructure.mappers.category_mapper import CategoryMapper


class CategoryRepositoryPostgres(CategoryRepository):
    """PostgreSQL-specific implementation of CategoryRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, category: Category) -> Category:
        """Save a category."""
        # PostgreSQL supports UUID natively, no conversion needed
        existing = self._session.query(CategoryORM).filter(
            CategoryORM.id == category.id
        ).first()
        
        if existing:
            existing.name = category.name
            existing.enabled = category.enabled
            existing.num_papers = category.num_papers
            self._session.commit()
            self._session.refresh(existing)
            return CategoryMapper.to_domain(existing)
        else:
            orm = CategoryMapper.to_orm(category)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return CategoryMapper.to_domain(orm)
    
    async def find_by_id(self, category_id: UUID) -> Optional[Category]:
        """Find category by ID."""
        # PostgreSQL supports UUID natively
        orm = self._session.query(CategoryORM).filter(
            CategoryORM.id == category_id
        ).first()
        
        return CategoryMapper.to_domain(orm) if orm else None
    
    async def find_by_name(self, name: str) -> Optional[Category]:
        """Find category by name."""
        orm = self._session.query(CategoryORM).filter(
            CategoryORM.name == name
        ).first()
        
        return CategoryMapper.to_domain(orm) if orm else None
    
    async def find_all(self, enabled_only: bool = False) -> List[Category]:
        """Find all categories."""
        query = self._session.query(CategoryORM)
        
        if enabled_only:
            query = query.filter(CategoryORM.enabled == True)
        
        orms = query.all()
        return [CategoryMapper.to_domain(orm) for orm in orms]

