"""Workflow plugin configuration repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.workflow.entities.workflow_plugin_config import WorkflowPluginConfig


class WorkflowPluginConfigRepository(ABC):
    """Abstract repository interface for WorkflowPluginConfig entity."""
    
    @abstractmethod
    async def save(self, config: WorkflowPluginConfig) -> WorkflowPluginConfig:
        """Save a workflow plugin configuration."""
        pass
    
    @abstractmethod
    async def find_by_id(self, config_id: UUID) -> Optional[WorkflowPluginConfig]:
        """Find workflow plugin config by ID."""
        pass
    
    @abstractmethod
    async def find_by_workflow_id(self, workflow_id: UUID) -> List[WorkflowPluginConfig]:
        """Find all plugin configs for a workflow."""
        pass
    
    @abstractmethod
    async def find_by_workflow_and_plugin(
        self,
        workflow_id: UUID,
        plugin_id: UUID,
    ) -> Optional[WorkflowPluginConfig]:
        """Find workflow plugin config by workflow and plugin IDs."""
        pass
    
    @abstractmethod
    async def delete(self, config_id: UUID) -> None:
        """Delete a workflow plugin configuration."""
        pass
    
    @abstractmethod
    async def delete_by_workflow_and_plugin(
        self,
        workflow_id: UUID,
        plugin_id: UUID,
    ) -> None:
        """Delete workflow plugin config by workflow and plugin IDs."""
        pass

