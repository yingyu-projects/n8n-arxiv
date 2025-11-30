"""Config repository implementation for PostgreSQL."""
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.config.entities.config import Config
from app.infrastructure.database.models.config_orm import ConfigORM
from app.infrastructure.mappers.config_mapper import ConfigMapper


class ConfigRepositoryPostgres(ConfigRepository):
    """PostgreSQL-specific implementation of ConfigRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, config: Config) -> Config:
        """Save a config."""
        # PostgreSQL supports UUID natively, no conversion needed
        existing = self._session.query(ConfigORM).filter(
            ConfigORM.id == config.id
        ).first()
        
        if existing:
            existing.key = config.key
            existing.value = config.value
            self._session.commit()
            self._session.refresh(existing)
            return ConfigMapper.to_domain(existing)
        else:
            orm = ConfigMapper.to_orm(config)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return ConfigMapper.to_domain(orm)
    
    async def find_by_id(self, config_id: UUID) -> Optional[Config]:
        """Find config by ID."""
        # PostgreSQL supports UUID natively
        orm = self._session.query(ConfigORM).filter(
            ConfigORM.id == config_id
        ).first()
        
        return ConfigMapper.to_domain(orm) if orm else None
    
    async def find_by_key(self, key: str) -> Optional[Config]:
        """Find config by key."""
        orm = self._session.query(ConfigORM).filter(
            ConfigORM.key == key
        ).first()
        
        return ConfigMapper.to_domain(orm) if orm else None

