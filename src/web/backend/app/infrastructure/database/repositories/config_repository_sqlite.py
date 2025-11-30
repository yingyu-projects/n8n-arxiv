"""Config repository implementation for SQLite."""
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.config.entities.config import Config
from app.infrastructure.database.models.config_orm import ConfigORM
from app.infrastructure.mappers.config_mapper import ConfigMapper


class ConfigRepositorySQLite(ConfigRepository):
    """SQLite-specific implementation of ConfigRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, config: Config) -> Config:
        """Save a config."""
        # Convert UUID to string for SQLite
        config_id = str(config.id)
        existing = self._session.query(ConfigORM).filter(
            ConfigORM.id == config_id
        ).first()
        
        if existing:
            existing.key = config.key
            existing.value = config.value
            self._session.commit()
            self._session.refresh(existing)
            return ConfigMapper.to_domain(existing)
        else:
            # Convert UUID to string for SQLite
            orm = ConfigMapper.to_orm(config, convert_uuid_to_string=True)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return ConfigMapper.to_domain(orm)
    
    async def find_by_id(self, config_id: UUID) -> Optional[Config]:
        """Find config by ID."""
        # Convert UUID to string for SQLite
        query_id = str(config_id)
        orm = self._session.query(ConfigORM).filter(
            ConfigORM.id == query_id
        ).first()
        
        return ConfigMapper.to_domain(orm) if orm else None
    
    async def find_by_key(self, key: str) -> Optional[Config]:
        """Find config by key."""
        orm = self._session.query(ConfigORM).filter(
            ConfigORM.key == key
        ).first()
        
        return ConfigMapper.to_domain(orm) if orm else None

