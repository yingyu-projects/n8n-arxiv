"""Mapper between Category ORM and Domain entity."""
import uuid
from app.domain.category.entities.category import Category
from app.infrastructure.database.models.category_orm import CategoryORM
from app.config import settings


class CategoryMapper:
    """Mapper for converting between Category ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def _ensure_string(id_value) -> str:
        """Convert UUID object to string if needed (for SQLite)."""
        if isinstance(id_value, uuid.UUID):
            return str(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: CategoryORM) -> Category:
        """Convert ORM model to domain entity."""
        return Category(
            id=CategoryMapper._ensure_uuid(orm.id),
            name=orm.name,
            enabled=orm.enabled,
            num_papers=orm.num_papers,
        )
    
    @staticmethod
    def to_orm(domain: Category) -> CategoryORM:
        """Convert domain entity to ORM model."""
        # Convert UUID to string if using SQLite
        is_sqlite = settings.database_url.startswith("sqlite")
        category_id = CategoryMapper._ensure_string(domain.id) if is_sqlite else domain.id
        
        return CategoryORM(
            id=category_id,
            name=domain.name,
            enabled=domain.enabled,
            num_papers=domain.num_papers,
        )

