"""Workflow repository implementation for PostgreSQL."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.domain.workflow.entities.workflow import Workflow
from app.infrastructure.database.models.workflow_orm import WorkflowORM
from app.infrastructure.mappers.workflow_mapper import WorkflowMapper


class WorkflowRepositoryPostgres(WorkflowRepository):
    """PostgreSQL-specific implementation of WorkflowRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, workflow: Workflow) -> Workflow:
        """Save a workflow."""
        existing = self._session.query(WorkflowORM).filter(
            WorkflowORM.id == workflow.id
        ).first()
        
        if existing:
            WorkflowMapper.update_orm_from_domain(existing, workflow)
            self._session.commit()
            self._session.refresh(existing)
            return WorkflowMapper.to_domain(existing)
        else:
            orm = WorkflowMapper.to_orm(workflow)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return WorkflowMapper.to_domain(orm)
    
    async def find_by_id(self, workflow_id: UUID) -> Optional[Workflow]:
        """Find workflow by ID."""
        orm = self._session.query(WorkflowORM).filter(
            WorkflowORM.id == workflow_id
        ).first()
        
        return WorkflowMapper.to_domain(orm) if orm else None
    
    async def find_by_name(self, name: str) -> Optional[Workflow]:
        """Find workflow by name."""
        orm = self._session.query(WorkflowORM).filter(
            WorkflowORM.name == name
        ).first()
        
        return WorkflowMapper.to_domain(orm) if orm else None
    
    async def find_all(self, enabled_only: bool = False, project_id: Optional[UUID] = None) -> List[Workflow]:
        """Find all workflows."""
        query = self._session.query(WorkflowORM)
        
        if enabled_only:
            query = query.filter(WorkflowORM.enabled == True)
        
        if project_id is not None:
            query = query.filter(WorkflowORM.project_id == project_id)
        
        query = query.order_by(WorkflowORM.created_at.desc())
        orms = query.all()
        return [WorkflowMapper.to_domain(orm) for orm in orms]
    
    async def delete(self, workflow_id: UUID) -> None:
        """Delete a workflow."""
        orm = self._session.query(WorkflowORM).filter(
            WorkflowORM.id == workflow_id
        ).first()
        
        if orm:
            self._session.delete(orm)
            self._session.commit()

