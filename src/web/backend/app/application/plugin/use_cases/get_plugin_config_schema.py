"""Get plugin config schema use case."""
from typing import Dict, Any, Optional
from uuid import UUID

from app.domain.plugin.repositories.plugin_repository import PluginRepository


class GetPluginConfigSchemaUseCase:
    """Use case for getting plugin configuration schema."""
    
    def __init__(self, plugin_repository: PluginRepository):
        """Initialize use case."""
        self._plugin_repository = plugin_repository
    
    async def execute(self, plugin_id: UUID) -> Optional[Dict[str, Any]]:
        """Execute use case - get plugin config schema.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            Config schema dictionary or None if plugin not found
        """
        plugin = await self._plugin_repository.find_by_id(plugin_id)
        
        if not plugin:
            return None
        
        return plugin.config_schema.to_dict()

