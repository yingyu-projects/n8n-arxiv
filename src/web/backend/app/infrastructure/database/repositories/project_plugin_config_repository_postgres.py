"""Project plugin config repository implementation for PostgreSQL."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository
from app.domain.project.entities.project_plugin_config import ProjectPluginConfig
from app.infrastructure.database.models.project_plugin_config_orm import ProjectPluginConfigORM
from app.infrastructure.mappers.project_plugin_config_mapper import ProjectPluginConfigMapper


class ProjectPluginConfigRepositoryPostgres(ProjectPluginConfigRepository):
    """PostgreSQL-specific implementation of ProjectPluginConfigRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, config: ProjectPluginConfig) -> ProjectPluginConfig:
        """Save a project plugin configuration."""
        existing = self._session.query(ProjectPluginConfigORM).filter(
            ProjectPluginConfigORM.id == config.id
        ).first()
        
        if existing:
            ProjectPluginConfigMapper.update_orm_from_domain(existing, config)
            self._session.commit()
            self._session.refresh(existing)
            return ProjectPluginConfigMapper.to_domain(existing)
        else:
            orm = ProjectPluginConfigMapper.to_orm(config)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return ProjectPluginConfigMapper.to_domain(orm)
    
    async def find_by_id(self, config_id: UUID) -> Optional[ProjectPluginConfig]:
        """Find project plugin config by ID."""
        orm = self._session.query(ProjectPluginConfigORM).filter(
            ProjectPluginConfigORM.id == config_id
        ).first()
        
        return ProjectPluginConfigMapper.to_domain(orm) if orm else None
    
    async def find_by_project_id(self, project_id: UUID) -> List[ProjectPluginConfig]:
        """Find all plugin configs for a project."""
        orms = self._session.query(ProjectPluginConfigORM).filter(
            ProjectPluginConfigORM.project_id == project_id
        ).all()
        
        return [ProjectPluginConfigMapper.to_domain(orm) for orm in orms]
    
    async def find_by_project_and_plugin(
        self,
        project_id: UUID,
        plugin_id: UUID,
    ) -> Optional[ProjectPluginConfig]:
        """Find project plugin config by project and plugin IDs."""
        orm = self._session.query(ProjectPluginConfigORM).filter(
            ProjectPluginConfigORM.project_id == project_id,
            ProjectPluginConfigORM.plugin_id == plugin_id,
        ).first()
        
        return ProjectPluginConfigMapper.to_domain(orm) if orm else None
    
    async def delete(self, config_id: UUID) -> None:
        """Delete a project plugin configuration."""
        orm = self._session.query(ProjectPluginConfigORM).filter(
            ProjectPluginConfigORM.id == config_id
        ).first()
        
        if orm:
            self._session.delete(orm)
            self._session.commit()
    
    async def delete_by_project_and_plugin(
        self,
        project_id: UUID,
        plugin_id: UUID,
    ) -> None:
        """Delete project plugin config by project and plugin IDs."""
        orm = self._session.query(ProjectPluginConfigORM).filter(
            ProjectPluginConfigORM.project_id == project_id,
            ProjectPluginConfigORM.plugin_id == plugin_id,
        ).first()
        
        if orm:
            self._session.delete(orm)
            self._session.commit()

