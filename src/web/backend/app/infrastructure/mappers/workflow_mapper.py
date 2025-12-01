"""Mapper between Workflow ORM and Domain entity."""
import uuid

from app.domain.workflow.entities.workflow import Workflow
from app.infrastructure.database.models.workflow_orm import WorkflowORM
from app.config import settings


class WorkflowMapper:
    """Mapper for converting between Workflow ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: WorkflowORM) -> Workflow:
        """Convert ORM model to domain entity."""
        return Workflow(
            id=WorkflowMapper._ensure_uuid(orm.id),
            name=orm.name,
            description=orm.description,
            categories=orm.categories or [],
            num_papers=orm.num_papers,
            enabled=orm.enabled,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
    
    @staticmethod
    def to_orm(domain: Workflow, convert_uuid_to_string: bool = False) -> WorkflowORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        workflow_id = str(domain.id) if convert_uuid_to_string else domain.id
        
        return WorkflowORM(
            id=workflow_id,
            name=domain.name,
            description=domain.description,
            categories=domain.categories,
            num_papers=domain.num_papers,
            enabled=domain.enabled,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: WorkflowORM, domain: Workflow) -> None:
        """Update ORM model from domain entity."""
        orm.name = domain.name
        orm.description = domain.description
        orm.categories = domain.categories
        orm.num_papers = domain.num_papers
        orm.enabled = domain.enabled
        orm.updated_at = domain.updated_at

