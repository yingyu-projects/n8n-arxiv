"""Project plugin configuration domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from uuid import UUID, uuid4


@dataclass
class ProjectPluginConfig:
    """Project plugin configuration entity."""
    
    id: UUID
    project_id: UUID
    plugin_id: UUID
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate entity."""
        if self.config is None:
            self.config = {}
    
    @classmethod
    def create(
        cls,
        project_id: UUID,
        plugin_id: UUID,
        config: Dict[str, Any] = None,
    ) -> "ProjectPluginConfig":
        """Factory method to create a new project plugin config."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            project_id=project_id,
            plugin_id=plugin_id,
            config=config or {},
            created_at=now,
            updated_at=now,
        )
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update plugin configuration."""
        if config is None:
            config = {}
        self.config = config
        self.updated_at = datetime.utcnow()

