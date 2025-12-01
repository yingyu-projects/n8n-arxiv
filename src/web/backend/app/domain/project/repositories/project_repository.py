"""Project repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.project.entities.project import Project


class ProjectRepository(ABC):
    """Abstract repository interface for Project entity."""
    
    @abstractmethod
    async def save(self, project: Project) -> Project:
        """Save a project."""
        pass
    
    @abstractmethod
    async def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """Find project by ID."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Project]:
        """Find project by name."""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Project]:
        """Find all projects."""
        pass
    
    @abstractmethod
    async def delete(self, project_id: UUID) -> None:
        """Delete a project."""
        pass


