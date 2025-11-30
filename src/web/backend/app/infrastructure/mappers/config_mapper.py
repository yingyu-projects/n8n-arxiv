"""Mapper between Config ORM and Domain entity."""
import uuid
from app.domain.config.entities.config import Config
from app.infrastructure.database.models.config_orm import ConfigORM


class ConfigMapper:
    """Mapper for converting between Config ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: ConfigORM) -> Config:
        """Convert ORM model to domain entity."""
        return Config(
            id=ConfigMapper._ensure_uuid(orm.id),
            key=orm.key,
            value=orm.value,
        )
    
    @staticmethod
    def to_orm(domain: Config, convert_uuid_to_string: bool = False) -> ConfigORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        config_id = str(domain.id) if convert_uuid_to_string else domain.id
        
        return ConfigORM(
            id=config_id,
            key=domain.key,
            value=domain.value,
        )

