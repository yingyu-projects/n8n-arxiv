"""Plugin execution repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.plugin.entities.plugin_execution import PluginExecution


class PluginExecutionRepository(ABC):
    """Abstract repository interface for PluginExecution entity."""
    
    @abstractmethod
    async def save(self, execution: PluginExecution) -> PluginExecution:
        """Save a plugin execution."""
        pass
    
    @abstractmethod
    async def find_by_id(self, execution_id: UUID) -> Optional[PluginExecution]:
        """Find plugin execution by ID."""
        pass
    
    @abstractmethod
    async def find_by_workflow_run_id(
        self,
        workflow_run_id: str,
    ) -> List[PluginExecution]:
        """Find all plugin executions for a workflow run."""
        pass
    
    @abstractmethod
    async def find_by_workflow_id(
        self,
        workflow_id: UUID,
        limit: int = 100,
    ) -> List[PluginExecution]:
        """Find recent plugin executions for a workflow."""
        pass

