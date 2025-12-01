"""Get all project plugin configs use case."""
from typing import List
from uuid import UUID

from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository
from app.application.dto.project_plugin_config_dto import ProjectPluginConfigDTO


class GetProjectPluginConfigsUseCase:
    """Use case for getting all plugin configs for a project."""
    
    def __init__(self, project_plugin_config_repository: ProjectPluginConfigRepository):
        """Initialize use case."""
        self._repository = project_plugin_config_repository
    
    async def execute(self, project_id: UUID) -> List[ProjectPluginConfigDTO]:
        """Execute use case - get all plugin configs for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            List of ProjectPluginConfigDTO
        """
        configs = await self._repository.find_by_project_id(project_id)
        return [ProjectPluginConfigDTO.from_domain(config) for config in configs]

