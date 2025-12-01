"""Plugin loader for discovering and loading plugins."""
import importlib
import inspect
import os
from pathlib import Path
from typing import List, Dict, Any, Type

from app.infrastructure.plugin.base_plugin import BasePlugin, OutputPlugin, InputPlugin, ProcessingPlugin


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
    
    def instantiate_plugin(self, plugin_class: Type[BasePlugin]) -> BasePlugin:
        """Instantiate a plugin class.
        
        Args:
            plugin_class: Plugin class to instantiate
            
        Returns:
            Plugin instance
        """
        return plugin_class()

