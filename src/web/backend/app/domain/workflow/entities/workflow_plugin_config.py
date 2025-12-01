"""Workflow plugin configuration domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from uuid import UUID, uuid4


@dataclass
class WorkflowPluginConfig:
    """Workflow plugin configuration entity."""
    
    id: UUID
    workflow_id: UUID
    plugin_id: UUID
    enabled: bool
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
        workflow_id: UUID,
        plugin_id: UUID,
        enabled: bool = True,
        config: Dict[str, Any] = None,
    ) -> "WorkflowPluginConfig":
        """Factory method to create a new workflow plugin config."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            workflow_id=workflow_id,
            plugin_id=plugin_id,
            enabled=enabled,
            config=config or {},
            created_at=now,
            updated_at=now,
        )
    
    def enable(self) -> None:
        """Enable plugin for this workflow."""
        self.enabled = True
        self.updated_at = datetime.utcnow()
    
    def disable(self) -> None:
        """Disable plugin for this workflow."""
        self.enabled = False
        self.updated_at = datetime.utcnow()
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update plugin configuration."""
        if config is None:
            config = {}
        self.config = config
        self.updated_at = datetime.utcnow()

