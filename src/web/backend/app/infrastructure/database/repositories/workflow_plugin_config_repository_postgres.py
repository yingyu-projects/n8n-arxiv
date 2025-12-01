"""Workflow plugin config repository implementation for PostgreSQL."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository
from app.domain.workflow.entities.workflow_plugin_config import WorkflowPluginConfig
from app.infrastructure.database.models.workflow_plugin_config_orm import WorkflowPluginConfigORM
from app.infrastructure.mappers.workflow_plugin_config_mapper import WorkflowPluginConfigMapper


class WorkflowPluginConfigRepositoryPostgres(WorkflowPluginConfigRepository):
    """PostgreSQL-specific implementation of WorkflowPluginConfigRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, config: WorkflowPluginConfig) -> WorkflowPluginConfig:
        """Save a workflow plugin configuration."""
        existing = self._session.query(WorkflowPluginConfigORM).filter(
            WorkflowPluginConfigORM.id == config.id
        ).first()
        
        if existing:
            WorkflowPluginConfigMapper.update_orm_from_domain(existing, config)
            self._session.commit()
            self._session.refresh(existing)
            return WorkflowPluginConfigMapper.to_domain(existing)
        else:
            orm = WorkflowPluginConfigMapper.to_orm(config)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return WorkflowPluginConfigMapper.to_domain(orm)
    
    async def find_by_id(self, config_id: UUID) -> Optional[WorkflowPluginConfig]:
        """Find workflow plugin config by ID."""
        orm = self._session.query(WorkflowPluginConfigORM).filter(
            WorkflowPluginConfigORM.id == config_id
        ).first()
        
        return WorkflowPluginConfigMapper.to_domain(orm) if orm else None
    
    async def find_by_workflow_id(self, workflow_id: UUID) -> List[WorkflowPluginConfig]:
        """Find all plugin configs for a workflow."""
        orms = self._session.query(WorkflowPluginConfigORM).filter(
            WorkflowPluginConfigORM.workflow_id == workflow_id
        ).all()
        
        return [WorkflowPluginConfigMapper.to_domain(orm) for orm in orms]
    
    async def find_by_workflow_and_plugin(
        self,
        workflow_id: UUID,
        plugin_id: UUID,
    ) -> Optional[WorkflowPluginConfig]:
        """Find workflow plugin config by workflow and plugin IDs."""
        orm = self._session.query(WorkflowPluginConfigORM).filter(
            WorkflowPluginConfigORM.workflow_id == workflow_id,
            WorkflowPluginConfigORM.plugin_id == plugin_id,
        ).first()
        
        return WorkflowPluginConfigMapper.to_domain(orm) if orm else None
    
    async def delete(self, config_id: UUID) -> None:
        """Delete a workflow plugin configuration."""
        orm = self._session.query(WorkflowPluginConfigORM).filter(
            WorkflowPluginConfigORM.id == config_id
        ).first()
        
        if orm:
            self._session.delete(orm)
            self._session.commit()
    
    async def delete_by_workflow_and_plugin(
        self,
        workflow_id: UUID,
        plugin_id: UUID,
    ) -> None:
        """Delete workflow plugin config by workflow and plugin IDs."""
        orm = self._session.query(WorkflowPluginConfigORM).filter(
            WorkflowPluginConfigORM.workflow_id == workflow_id,
            WorkflowPluginConfigORM.plugin_id == plugin_id,
        ).first()
        
        if orm:
            self._session.delete(orm)
            self._session.commit()

