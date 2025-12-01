"""Get plugins use case."""
from typing import List, Optional

from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.value_objects.plugin_type import PluginType
from app.application.dto.plugin_dto import PluginDTO


class GetPluginsUseCase:
    """Use case for getting plugins."""
    
    def __init__(self, plugin_repository: PluginRepository):
        """Initialize use case."""
        self._plugin_repository = plugin_repository
    
    async def execute(
        self,
        plugin_type: Optional[PluginType] = None,
        enabled_only: bool = False,
    ) -> List[PluginDTO]:
        """Execute use case - get plugins.
        
        Args:
            plugin_type: Optional plugin type filter
            enabled_only: Only return enabled plugins
            
        Returns:
            List of PluginDTO
        """
        plugins = await self._plugin_repository.find_all(
            plugin_type=plugin_type,
            enabled_only=enabled_only,
        )
        
        return [PluginDTO.from_domain(plugin) for plugin in plugins]

