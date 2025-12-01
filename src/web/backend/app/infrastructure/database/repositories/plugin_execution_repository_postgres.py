"""Plugin execution repository implementation for PostgreSQL."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.plugin.repositories.plugin_execution_repository import PluginExecutionRepository
from app.domain.plugin.entities.plugin_execution import PluginExecution
from app.infrastructure.database.models.plugin_execution_orm import PluginExecutionORM
from app.infrastructure.mappers.plugin_execution_mapper import PluginExecutionMapper


class PluginExecutionRepositoryPostgres(PluginExecutionRepository):
    """PostgreSQL-specific implementation of PluginExecutionRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, execution: PluginExecution) -> PluginExecution:
        """Save a plugin execution."""
        existing = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.id == execution.id
        ).first()
        
        if existing:
            PluginExecutionMapper.update_orm_from_domain(existing, execution)
            self._session.commit()
            self._session.refresh(existing)
            return PluginExecutionMapper.to_domain(existing)
        else:
            orm = PluginExecutionMapper.to_orm(execution)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return PluginExecutionMapper.to_domain(orm)
    
    async def find_by_id(self, execution_id: UUID) -> Optional[PluginExecution]:
        """Find plugin execution by ID."""
        orm = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.id == execution_id
        ).first()
        
        return PluginExecutionMapper.to_domain(orm) if orm else None
    
    async def find_by_workflow_run_id(
        self,
        workflow_run_id: str,
    ) -> List[PluginExecution]:
        """Find all plugin executions for a workflow run."""
        orms = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.workflow_run_id == workflow_run_id
        ).order_by(PluginExecutionORM.started_at.desc()).all()
        
        return [PluginExecutionMapper.to_domain(orm) for orm in orms]
    
    async def find_by_workflow_id(
        self,
        workflow_id: UUID,
        limit: int = 100,
    ) -> List[PluginExecution]:
        """Find recent plugin executions for a workflow."""
        orms = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.workflow_id == workflow_id
        ).order_by(PluginExecutionORM.started_at.desc()).limit(limit).all()
        
        return [PluginExecutionMapper.to_domain(orm) for orm in orms]

