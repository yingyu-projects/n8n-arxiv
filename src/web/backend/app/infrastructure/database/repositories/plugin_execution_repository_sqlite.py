"""Plugin execution repository implementation for SQLite."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.plugin.repositories.plugin_execution_repository import PluginExecutionRepository
from app.domain.plugin.entities.plugin_execution import PluginExecution
from app.infrastructure.database.models.plugin_execution_orm import PluginExecutionORM
from app.infrastructure.mappers.plugin_execution_mapper import PluginExecutionMapper


class PluginExecutionRepositorySQLite(PluginExecutionRepository):
    """SQLite-specific implementation of PluginExecutionRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, execution: PluginExecution) -> PluginExecution:
        """Save a plugin execution."""
        execution_id = str(execution.id)
        existing = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.id == execution_id
        ).first()
        
        if existing:
            PluginExecutionMapper.update_orm_from_domain(existing, execution)
            self._session.commit()
            self._session.refresh(existing)
            return PluginExecutionMapper.to_domain(existing)
        else:
            orm = PluginExecutionMapper.to_orm(execution, convert_uuid_to_string=True)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return PluginExecutionMapper.to_domain(orm)
    
    async def find_by_id(self, execution_id: UUID) -> Optional[PluginExecution]:
        """Find plugin execution by ID."""
        query_id = str(execution_id)
        orm = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.id == query_id
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
        query_id = str(workflow_id)
        orms = self._session.query(PluginExecutionORM).filter(
            PluginExecutionORM.workflow_id == query_id
        ).order_by(PluginExecutionORM.started_at.desc()).limit(limit).all()
        
        return [PluginExecutionMapper.to_domain(orm) for orm in orms]

