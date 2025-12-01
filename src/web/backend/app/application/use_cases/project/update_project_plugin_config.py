"""Update project plugin config use case."""
from typing import Dict, Any
from uuid import UUID

from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository
from app.domain.project.entities.project_plugin_config import ProjectPluginConfig
from app.application.dto.project_plugin_config_dto import ProjectPluginConfigDTO


class UpdateProjectPluginConfigUseCase:
    """Use case for updating a project plugin config."""
    
    def __init__(self, project_plugin_config_repository: ProjectPluginConfigRepository):
        """Initialize use case."""
        self._repository = project_plugin_config_repository
    
    async def execute(
        self,
        project_id: UUID,
        plugin_id: UUID,
        config: Dict[str, Any],
    ) -> ProjectPluginConfigDTO:
        """Execute use case - update or create a project plugin config.
        
        Args:
            project_id: Project ID
            plugin_id: Plugin ID
            config: Plugin configuration values
            
        Returns:
            ProjectPluginConfigDTO
        """
        existing = await self._repository.find_by_project_and_plugin(project_id, plugin_id)
        
        if existing:
            existing.update_config(config)
            updated = await self._repository.save(existing)
        else:
            new_config = ProjectPluginConfig.create(
                project_id=project_id,
                plugin_id=plugin_id,
                config=config,
            )
            updated = await self._repository.save(new_config)
        
        return ProjectPluginConfigDTO.from_domain(updated)

