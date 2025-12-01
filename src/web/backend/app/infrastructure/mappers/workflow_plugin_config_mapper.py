"""Mapper between WorkflowPluginConfig ORM and Domain entity."""
import uuid

from app.domain.workflow.entities.workflow_plugin_config import WorkflowPluginConfig
from app.infrastructure.database.models.workflow_plugin_config_orm import WorkflowPluginConfigORM
from app.config import settings


class WorkflowPluginConfigMapper:
    """Mapper for converting between WorkflowPluginConfig ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: WorkflowPluginConfigORM) -> WorkflowPluginConfig:
        """Convert ORM model to domain entity."""
        return WorkflowPluginConfig(
            id=WorkflowPluginConfigMapper._ensure_uuid(orm.id),
            workflow_id=WorkflowPluginConfigMapper._ensure_uuid(orm.workflow_id),
            plugin_id=WorkflowPluginConfigMapper._ensure_uuid(orm.plugin_id),
            enabled=orm.enabled,
            config=orm.config or {},
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
    
    @staticmethod
    def to_orm(domain: WorkflowPluginConfig, convert_uuid_to_string: bool = False) -> WorkflowPluginConfigORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        config_id = str(domain.id) if convert_uuid_to_string else domain.id
        workflow_id = str(domain.workflow_id) if convert_uuid_to_string else domain.workflow_id
        plugin_id = str(domain.plugin_id) if convert_uuid_to_string else domain.plugin_id
        
        return WorkflowPluginConfigORM(
            id=config_id,
            workflow_id=workflow_id,
            plugin_id=plugin_id,
            enabled=domain.enabled,
            config=domain.config,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: WorkflowPluginConfigORM, domain: WorkflowPluginConfig) -> None:
        """Update ORM model from domain entity."""
        orm.enabled = domain.enabled
        orm.config = domain.config
        orm.updated_at = domain.updated_at

