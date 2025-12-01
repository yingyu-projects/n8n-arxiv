"""Project plugin config DTO."""
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID
from datetime import datetime

from app.domain.project.entities.project_plugin_config import ProjectPluginConfig


@dataclass
class ProjectPluginConfigDTO:
    """Data transfer object for ProjectPluginConfig."""
    
    id: UUID
    project_id: UUID
    plugin_id: UUID
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, config: ProjectPluginConfig) -> "ProjectPluginConfigDTO":
        """Create DTO from domain entity."""
        return cls(
            id=config.id,
            project_id=config.project_id,
            plugin_id=config.plugin_id,
            config=config.config,
            created_at=config.created_at,
            updated_at=config.updated_at,
        )

