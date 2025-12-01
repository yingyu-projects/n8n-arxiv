"""Plugin domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID, uuid4

from app.domain.plugin.value_objects.plugin_type import PluginType
from app.domain.plugin.value_objects.config_schema import ConfigSchema


@dataclass
class Plugin:
    """Plugin domain entity with business logic."""
    
    id: UUID
    name: str
    type: PluginType
    version: str
    config_schema: ConfigSchema
    enabled: bool
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate entity."""
        if not self.name:
            raise ValueError("Plugin name cannot be empty")
        if not self.version:
            raise ValueError("Plugin version cannot be empty")
    
    @classmethod
    def create(
        cls,
        name: str,
        type: PluginType,
        version: str,
        config_schema: ConfigSchema,
        enabled: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Plugin":
        """Factory method to create a new plugin."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            name=name,
            type=type,
            version=version,
            config_schema=config_schema,
            enabled=enabled,
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )
    
    def enable(self) -> None:
        """Enable plugin."""
        self.enabled = True
        self.updated_at = datetime.utcnow()
    
    def disable(self) -> None:
        """Disable plugin."""
        self.enabled = False
        self.updated_at = datetime.utcnow()
    
    def update_config_schema(self, config_schema: ConfigSchema) -> None:
        """Update plugin configuration schema."""
        self.config_schema = config_schema
        self.updated_at = datetime.utcnow()
    
    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update plugin metadata."""
        self.metadata = metadata or {}
        self.updated_at = datetime.utcnow()

