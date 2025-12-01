"""Plugin DTO."""
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID

from app.domain.plugin.entities.plugin import Plugin
from app.domain.plugin.value_objects.plugin_type import PluginType


@dataclass
class PluginDTO:
    """Data transfer object for Plugin."""
    
    id: UUID
    name: str
    type: PluginType
    version: str
    config_schema: Dict[str, Any]
    enabled: bool
    metadata: Dict[str, Any]
    
    @classmethod
    def from_domain(cls, plugin: Plugin) -> "PluginDTO":
        """Create DTO from domain entity."""
        return cls(
            id=plugin.id,
            name=plugin.name,
            type=plugin.type,
            version=plugin.version,
            config_schema=plugin.config_schema.to_dict(),
            enabled=plugin.enabled,
            metadata=plugin.metadata,
        )

