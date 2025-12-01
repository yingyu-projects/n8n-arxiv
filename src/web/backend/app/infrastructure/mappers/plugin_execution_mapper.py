"""Mapper between PluginExecution ORM and Domain entity."""
import uuid

from app.domain.plugin.entities.plugin_execution import PluginExecution
from app.domain.plugin.value_objects.plugin_status import PluginStatus
from app.infrastructure.database.models.plugin_execution_orm import PluginExecutionORM
from app.config import settings


class PluginExecutionMapper:
    """Mapper for converting between PluginExecution ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: PluginExecutionORM) -> PluginExecution:
        """Convert ORM model to domain entity."""
        return PluginExecution(
            id=PluginExecutionMapper._ensure_uuid(orm.id),
            plugin_id=PluginExecutionMapper._ensure_uuid(orm.plugin_id),
            workflow_id=PluginExecutionMapper._ensure_uuid(orm.workflow_id),
            workflow_run_id=orm.workflow_run_id,
            paper_id=PluginExecutionMapper._ensure_uuid(orm.paper_id),
            status=PluginStatus(orm.status),
            config=orm.config or {},
            result=orm.result,
            started_at=orm.started_at,
            completed_at=orm.completed_at,
        )
    
    @staticmethod
    def to_orm(domain: PluginExecution, convert_uuid_to_string: bool = False) -> PluginExecutionORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        execution_id = str(domain.id) if convert_uuid_to_string else domain.id
        plugin_id = str(domain.plugin_id) if convert_uuid_to_string else domain.plugin_id
        workflow_id = str(domain.workflow_id) if convert_uuid_to_string else domain.workflow_id
        paper_id = str(domain.paper_id) if convert_uuid_to_string else domain.paper_id
        
        return PluginExecutionORM(
            id=execution_id,
            plugin_id=plugin_id,
            workflow_id=workflow_id,
            workflow_run_id=domain.workflow_run_id,
            paper_id=paper_id,
            status=domain.status.value,
            config=domain.config,
            result=domain.result,
            started_at=domain.started_at,
            completed_at=domain.completed_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: PluginExecutionORM, domain: PluginExecution) -> None:
        """Update ORM model from domain entity."""
        orm.status = domain.status.value
        orm.config = domain.config
        orm.result = domain.result
        orm.completed_at = domain.completed_at

