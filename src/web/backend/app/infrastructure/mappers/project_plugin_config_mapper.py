"""Mapper between ProjectPluginConfig ORM and Domain entity."""
import uuid

from app.domain.project.entities.project_plugin_config import ProjectPluginConfig
from app.infrastructure.database.models.project_plugin_config_orm import ProjectPluginConfigORM
from app.config import settings


class ProjectPluginConfigMapper:
    """Mapper for converting between ProjectPluginConfig ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: ProjectPluginConfigORM) -> ProjectPluginConfig:
        """Convert ORM model to domain entity."""
        return ProjectPluginConfig(
            id=ProjectPluginConfigMapper._ensure_uuid(orm.id),
            project_id=ProjectPluginConfigMapper._ensure_uuid(orm.project_id),
            plugin_id=ProjectPluginConfigMapper._ensure_uuid(orm.plugin_id),
            config=orm.config or {},
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
    
    @staticmethod
    def to_orm(domain: ProjectPluginConfig, convert_uuid_to_string: bool = False) -> ProjectPluginConfigORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        config_id = str(domain.id) if convert_uuid_to_string else domain.id
        project_id = str(domain.project_id) if convert_uuid_to_string else domain.project_id
        plugin_id = str(domain.plugin_id) if convert_uuid_to_string else domain.plugin_id
        
        return ProjectPluginConfigORM(
            id=config_id,
            project_id=project_id,
            plugin_id=plugin_id,
            config=domain.config,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: ProjectPluginConfigORM, domain: ProjectPluginConfig) -> None:
        """Update ORM model from domain entity."""
        orm.config = domain.config
        orm.updated_at = domain.updated_at

