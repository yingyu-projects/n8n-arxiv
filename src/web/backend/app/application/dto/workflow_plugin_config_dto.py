"""Workflow plugin config DTO."""
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID
from datetime import datetime

from app.domain.workflow.entities.workflow_plugin_config import WorkflowPluginConfig


@dataclass
class WorkflowPluginConfigDTO:
    """Data transfer object for WorkflowPluginConfig."""
    
    id: UUID
    workflow_id: UUID
    plugin_id: UUID
    enabled: bool
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, config: WorkflowPluginConfig) -> "WorkflowPluginConfigDTO":
        """Create DTO from domain entity."""
        return cls(
            id=config.id,
            workflow_id=config.workflow_id,
            plugin_id=config.plugin_id,
            enabled=config.enabled,
            config=config.config,
            created_at=config.created_at,
            updated_at=config.updated_at,
        )

