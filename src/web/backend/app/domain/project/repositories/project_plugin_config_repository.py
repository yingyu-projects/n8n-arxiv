"""Project plugin configuration repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.project.entities.project_plugin_config import ProjectPluginConfig


class ProjectPluginConfigRepository(ABC):
    """Abstract repository interface for ProjectPluginConfig entity."""
    
    @abstractmethod
    async def save(self, config: ProjectPluginConfig) -> ProjectPluginConfig:
        """Save a project plugin configuration."""
        pass
    
    @abstractmethod
    async def find_by_id(self, config_id: UUID) -> Optional[ProjectPluginConfig]:
        """Find project plugin config by ID."""
        pass
    
    @abstractmethod
    async def find_by_project_id(self, project_id: UUID) -> List[ProjectPluginConfig]:
        """Find all plugin configs for a project."""
        pass
    
    @abstractmethod
    async def find_by_project_and_plugin(
        self,
        project_id: UUID,
        plugin_id: UUID,
    ) -> Optional[ProjectPluginConfig]:
        """Find project plugin config by project and plugin IDs."""
        pass
    
    @abstractmethod
    async def delete(self, config_id: UUID) -> None:
        """Delete a project plugin configuration."""
        pass
    
    @abstractmethod
    async def delete_by_project_and_plugin(
        self,
        project_id: UUID,
        plugin_id: UUID,
    ) -> None:
        """Delete project plugin config by project and plugin IDs."""
        pass

