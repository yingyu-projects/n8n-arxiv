"""Workflow repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.workflow.entities.workflow import Workflow


class WorkflowRepository(ABC):
    """Abstract repository interface for Workflow entity."""
    
    @abstractmethod
    async def save(self, workflow: Workflow) -> Workflow:
        """Save a workflow."""
        pass
    
    @abstractmethod
    async def find_by_id(self, workflow_id: UUID) -> Optional[Workflow]:
        """Find workflow by ID."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Workflow]:
        """Find workflow by name."""
        pass
    
    @abstractmethod
    async def find_all(self, enabled_only: bool = False) -> List[Workflow]:
        """Find all workflows."""
        pass
    
    @abstractmethod
    async def delete(self, workflow_id: UUID) -> None:
        """Delete a workflow."""
        pass

