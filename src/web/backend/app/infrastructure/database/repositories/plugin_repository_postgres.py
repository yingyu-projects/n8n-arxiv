"""Plugin repository implementation for PostgreSQL."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.entities.plugin import Plugin
from app.domain.plugin.value_objects.plugin_type import PluginType
from app.infrastructure.database.models.plugin_orm import PluginORM
from app.infrastructure.mappers.plugin_mapper import PluginMapper


class PluginRepositoryPostgres(PluginRepository):
    """PostgreSQL-specific implementation of PluginRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, plugin: Plugin) -> Plugin:
        """Save a plugin."""
        existing = self._session.query(PluginORM).filter(
            PluginORM.id == plugin.id
        ).first()
        
        if existing:
            PluginMapper.update_orm_from_domain(existing, plugin)
            self._session.commit()
            self._session.refresh(existing)
            return PluginMapper.to_domain(existing)
        else:
            orm = PluginMapper.to_orm(plugin)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return PluginMapper.to_domain(orm)
    
    async def find_by_id(self, plugin_id: UUID) -> Optional[Plugin]:
        """Find plugin by ID."""
        orm = self._session.query(PluginORM).filter(
            PluginORM.id == plugin_id
        ).first()
        
        return PluginMapper.to_domain(orm) if orm else None
    
    async def find_by_name(self, name: str) -> Optional[Plugin]:
        """Find plugin by name."""
        orm = self._session.query(PluginORM).filter(
            PluginORM.name == name
        ).first()
        
        return PluginMapper.to_domain(orm) if orm else None
    
    async def find_all(
        self,
        plugin_type: Optional[PluginType] = None,
        enabled_only: bool = False,
    ) -> List[Plugin]:
        """Find all plugins with optional filtering."""
        query = self._session.query(PluginORM)
        
        if plugin_type:
            query = query.filter(PluginORM.type == plugin_type.value)
        
        if enabled_only:
            query = query.filter(PluginORM.enabled == True)
        
        query = query.order_by(PluginORM.name)
        orms = query.all()
        return [PluginMapper.to_domain(orm) for orm in orms]

