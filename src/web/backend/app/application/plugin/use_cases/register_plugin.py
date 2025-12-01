"""Register plugin use case."""
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.entities.plugin import Plugin
from app.domain.plugin.value_objects.plugin_type import PluginType
from app.domain.plugin.value_objects.config_schema import ConfigSchema
from app.application.dto.plugin_dto import PluginDTO


class RegisterPluginUseCase:
    """Use case for registering a plugin."""
    
    def __init__(self, plugin_repository: PluginRepository):
        """Initialize use case."""
        self._plugin_repository = plugin_repository
    
    async def execute(
        self,
        name: str,
        plugin_type: PluginType,
        version: str,
        config_schema: ConfigSchema,
        metadata: dict = None,
    ) -> PluginDTO:
        """Execute use case - register a plugin.
        
        Args:
            name: Plugin name
            plugin_type: Plugin type
            version: Plugin version
            config_schema: Configuration schema
            metadata: Optional metadata
            
        Returns:
            PluginDTO
        """
        # Check if plugin already exists
        existing = await self._plugin_repository.find_by_name(name)
        
        if existing:
            # Update existing plugin
            existing.update_config_schema(config_schema)
            if metadata:
                existing.update_metadata(metadata)
            plugin = await self._plugin_repository.save(existing)
        else:
            # Create new plugin
            plugin = Plugin.create(
                name=name,
                type=plugin_type,
                version=version,
                config_schema=config_schema,
                metadata=metadata,
            )
            plugin = await self._plugin_repository.save(plugin)
        
        return PluginDTO.from_domain(plugin)

