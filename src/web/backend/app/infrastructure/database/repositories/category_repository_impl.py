"""Category repository implementation using SQLAlchemy."""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.category.entities.category import Category
from app.domain.category.repositories.category_repository import CategoryRepository
from app.infrastructure.database.models.category_orm import CategoryORM
from app.infrastructure.mappers.category_mapper import CategoryMapper
from app.config import settings


class CategoryRepositoryImpl(CategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    def _convert_id_for_query(self, category_id: UUID):
        """Convert UUID to string if using SQLite."""
        is_sqlite = settings.database_url.startswith("sqlite")
        return str(category_id) if is_sqlite else category_id
    
    async def save(self, category: Category) -> Category:
        """Save a category."""
        # Convert UUID to string for SQLite compatibility
        category_id = self._convert_id_for_query(category.id)
        existing = self._session.query(CategoryORM).filter(
            CategoryORM.id == category_id
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
        # Convert UUID to string for SQLite compatibility
        query_id = self._convert_id_for_query(category_id)
        orm = self._session.query(CategoryORM).filter(
            CategoryORM.id == query_id
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

