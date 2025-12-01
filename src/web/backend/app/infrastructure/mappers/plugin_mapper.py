"""Mapper between Plugin ORM and Domain entity."""
import uuid

from app.domain.plugin.entities.plugin import Plugin
from app.domain.plugin.value_objects.plugin_type import PluginType
from app.domain.plugin.value_objects.config_schema import ConfigSchema
from app.infrastructure.database.models.plugin_orm import PluginORM
from app.config import settings


class PluginMapper:
    """Mapper for converting between Plugin ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: PluginORM) -> Plugin:
        """Convert ORM model to domain entity."""
        return Plugin(
            id=PluginMapper._ensure_uuid(orm.id),
            name=orm.name,
            type=PluginType(orm.type),
            version=orm.version,
            config_schema=ConfigSchema.from_dict(orm.config_schema),
            enabled=orm.enabled,
            metadata=orm.plugin_metadata or {},
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
    
    @staticmethod
    def to_orm(domain: Plugin, convert_uuid_to_string: bool = False) -> PluginORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        plugin_id = str(domain.id) if convert_uuid_to_string else domain.id
        
        return PluginORM(
            id=plugin_id,
            name=domain.name,
            type=domain.type.value,
            version=domain.version,
            config_schema=domain.config_schema.to_dict(),
            enabled=domain.enabled,
            plugin_metadata=domain.metadata,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: PluginORM, domain: Plugin) -> None:
        """Update ORM model from domain entity."""
        orm.name = domain.name
        orm.type = domain.type.value
        orm.version = domain.version
        orm.config_schema = domain.config_schema.to_dict()
        orm.enabled = domain.enabled
        orm.plugin_metadata = domain.metadata
        orm.updated_at = domain.updated_at

