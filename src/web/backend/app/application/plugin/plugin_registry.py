"""Plugin registry for managing plugin discovery and registration."""
from typing import Dict, Optional
from uuid import UUID

from app.domain.plugin.entities.plugin import Plugin
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.infrastructure.plugin.plugin_loader import PluginLoader
from app.infrastructure.plugin.base_plugin import BasePlugin


class PluginRegistry:
    """Registry for managing plugins."""
    
    def __init__(
        self,
        plugin_repository: PluginRepository,
        plugin_loader: PluginLoader = None,
    ):
        """Initialize plugin registry.
        
        Args:
            plugin_repository: Repository for plugin persistence
            plugin_loader: Plugin loader instance
        """
        self._plugin_repository = plugin_repository
        self._plugin_loader = plugin_loader or PluginLoader()
        self._plugin_instances: Dict[str, BasePlugin] = {}
    
    async def discover_and_register_plugins(self) -> list[Plugin]:
        """Discover plugins from filesystem and register them in database.
        
        Returns:
            List of registered plugins
        """
        plugin_classes = self._plugin_loader.discover_plugins()
        registered = []
        
        for plugin_class in plugin_classes:
            try:
                plugin_instance = self._plugin_loader.instantiate_plugin(plugin_class)
                
                # Check if plugin already exists
                existing = await self._plugin_repository.find_by_name(plugin_instance.name)
                
                if existing:
                    # Update existing plugin
                    existing.update_config_schema(plugin_instance.get_config_schema())
                    existing.update_metadata(plugin_instance.get_metadata())
                    plugin = await self._plugin_repository.save(existing)
                else:
                    # Create new plugin
                    from app.domain.plugin.value_objects.config_schema import ConfigSchema
                    plugin = Plugin.create(
                        name=plugin_instance.name,
                        type=plugin_instance.plugin_type,
                        version=plugin_instance.version,
                        config_schema=plugin_instance.get_config_schema(),
                        metadata=plugin_instance.get_metadata(),
                    )
                    plugin = await self._plugin_repository.save(plugin)
                
                # Cache plugin instance
                self._plugin_instances[str(plugin.id)] = plugin_instance
                registered.append(plugin)
            
            except Exception as e:
                print(f"Error registering plugin {plugin_class}: {e}")
                continue
        
        return registered
    
    async def get_plugin_instance(self, plugin_id: UUID) -> Optional[BasePlugin]:
        """Get plugin instance by ID.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            Plugin instance or None if not found
        """
        # Check cache first
        cache_key = str(plugin_id)
        if cache_key in self._plugin_instances:
            return self._plugin_instances[cache_key]
        
        # Load from repository and instantiate
        plugin = await self._plugin_repository.find_by_id(plugin_id)
        if not plugin:
            return None
        
        # Find plugin class and instantiate
        plugin_classes = self._plugin_loader.discover_plugins()
        for plugin_class in plugin_classes:
            instance = self._plugin_loader.instantiate_plugin(plugin_class)
            if instance.name == plugin.name:
                self._plugin_instances[cache_key] = instance
                return instance
        
        return None

