"""Plugin loader for discovering and loading plugins."""
import importlib
import inspect
import os
from pathlib import Path
from typing import List, Dict, Any, Type, Optional

from app.infrastructure.plugin.base_plugin import BasePlugin, OutputPlugin, InputPlugin, ProcessingPlugin
from app.application.plugin.core_api import CoreAPI


class PluginLoader:
    """Loads plugins from the plugins directory."""
    
    def __init__(self, plugins_dir: str = None):
        """Initialize plugin loader.
        
        Args:
            plugins_dir: Path to plugins directory. If None, uses default location.
        """
        if plugins_dir is None:
            # Default to app/infrastructure/plugin/plugins
            base_path = Path(__file__).parent
            plugins_dir = str(base_path / "plugins")
        
        self.plugins_dir = Path(plugins_dir)
    
    def discover_plugins(self) -> List[Type[BasePlugin]]:
        """Discover all plugins in the plugins directory.
        
        Returns:
            List of plugin classes
        """
        plugins = []
        
        if not self.plugins_dir.exists():
            return plugins
        
        # Iterate through plugin directories
        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith('_'):
                continue
            
            # Look for __init__.py
            init_file = plugin_dir / "__init__.py"
            if not init_file.exists():
                continue
            
            # Try to import the plugin module
            try:
                module_name = f"app.infrastructure.plugin.plugins.{plugin_dir.name}"
                module = importlib.import_module(module_name)
                
                # Find plugin classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(obj, BasePlugin) and 
                        obj != BasePlugin and 
                        obj != OutputPlugin and 
                        obj != InputPlugin and 
                        obj != ProcessingPlugin):
                        plugins.append(obj)
            
            except Exception as e:
                # Log error but continue
                print(f"Error loading plugin from {plugin_dir}: {e}")
                continue
        
        return plugins
    
    def instantiate_plugin(
        self, 
        plugin_class: Type[BasePlugin],
        core_api: Optional[CoreAPI] = None
    ) -> BasePlugin:
        """Instantiate a plugin class.
        
        Args:
            plugin_class: Plugin class to instantiate
            core_api: Optional CoreAPI instance to inject
            
        Returns:
            Plugin instance
        """
        # Try to instantiate with core_api parameter
        if core_api is not None:
            try:
                # Check if plugin accepts core_api parameter
                import inspect
                sig = inspect.signature(plugin_class.__init__)
                if 'core_api' in sig.parameters:
                    return plugin_class(core_api=core_api)
            except (TypeError, AttributeError):
                # Fallback to default instantiation
                pass
        
        # Fallback: instantiate without core_api (backward compatibility)
        instance = plugin_class()
        
        # If core_api is provided, inject it via protected attribute
        if core_api is not None:
            instance._core_api = core_api
        
        return instance

