"""Get project plugin config use case."""
from typing import Optional
from uuid import UUID

from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository
from app.application.dto.project_plugin_config_dto import ProjectPluginConfigDTO


class GetProjectPluginConfigUseCase:
    """Use case for getting a project plugin config by project and plugin IDs."""
    
    def __init__(self, project_plugin_config_repository: ProjectPluginConfigRepository):
        """Initialize use case."""
        self._repository = project_plugin_config_repository
    
    async def execute(
        self,
        project_id: UUID,
        plugin_id: UUID,
    ) -> Optional[ProjectPluginConfigDTO]:
        """Execute use case - get project plugin config by project and plugin IDs.
        
        Args:
            project_id: Project ID
            plugin_id: Plugin ID
            
        Returns:
            ProjectPluginConfigDTO or None if not found
        """
        config = await self._repository.find_by_project_and_plugin(project_id, plugin_id)
        return ProjectPluginConfigDTO.from_domain(config) if config else None

