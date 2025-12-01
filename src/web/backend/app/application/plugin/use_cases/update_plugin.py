"""Update plugin use case."""
from uuid import UUID

from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.application.dto.plugin_dto import PluginDTO


class UpdatePluginUseCase:
    """Use case for updating plugins."""
    
    def __init__(self, plugin_repository: PluginRepository):
        """Initialize use case."""
        self._plugin_repository = plugin_repository
    
    async def execute(
        self,
        plugin_id: UUID,
        enabled: bool = None,
    ) -> PluginDTO:
        """Execute use case - update plugin.
        
        Args:
            plugin_id: Plugin ID
            enabled: Optional enabled status to update
            
        Returns:
            PluginDTO
        """
        plugin = await self._plugin_repository.find_by_id(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin with ID {plugin_id} not found")
        
        if enabled is not None:
            if enabled:
                plugin.enable()
            else:
                plugin.disable()
        
        updated_plugin = await self._plugin_repository.save(plugin)
        return PluginDTO.from_domain(updated_plugin)


