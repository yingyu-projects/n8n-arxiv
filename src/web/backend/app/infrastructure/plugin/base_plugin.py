"""Base plugin classes."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.domain.paper.entities.paper import Paper
from app.domain.plugin.value_objects.config_schema import ConfigSchema
from app.domain.plugin.value_objects.plugin_type import PluginType
from app.application.plugin.core_api import CoreAPI


class BasePlugin(ABC):
    """Base class for all plugins."""
    
    def __init__(
        self, 
        name: str, 
        version: str, 
        plugin_type: PluginType, 
        metadata: Dict[str, Any] = None,
        core_api: Optional[CoreAPI] = None
    ):
        """Initialize plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
            plugin_type: Plugin type
            metadata: Optional plugin metadata
            core_api: Core API instance (injected by plugin registry)
        """
        self.name = name
        self.version = version
        self.plugin_type = plugin_type
        self.metadata = metadata or {}
        self._core_api = core_api
    
    @property
    def api(self) -> CoreAPI:
        """Get the Core API instance.
        
        Raises:
            RuntimeError: If CoreAPI is not set
        """
        if self._core_api is None:
            raise RuntimeError(
                f"CoreAPI not initialized for plugin {self.name}. "
                "Plugins must be instantiated through PluginRegistry."
            )
        return self._core_api
    
    @abstractmethod
    def get_config_schema(self) -> ConfigSchema:
        """Get plugin configuration schema.
        
        Returns:
            ConfigSchema: JSON schema defining the plugin's configuration fields
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get plugin metadata.
        
        Returns:
            Dict containing plugin metadata
        """
        return self.metadata


class OutputPlugin(BasePlugin):
    """Base class for output plugins (e.g., Slack, email, webhook)."""
    
    def __init__(
        self, 
        name: str, 
        version: str, 
        metadata: Dict[str, Any] = None,
        core_api: Optional[CoreAPI] = None
    ):
        """Initialize output plugin."""
        super().__init__(name, version, PluginType.OUTPUT, metadata, core_api)
    
    @abstractmethod
    async def execute(self, paper: Paper, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the plugin with the given paper and configuration.
        
        Args:
            paper: The parsed paper entity
            config: Plugin configuration values
            
        Returns:
            Dict containing execution result
        """
        pass


class InputPlugin(BasePlugin):
    """Base class for input plugins (alternative paper sources)."""
    
    def __init__(
        self, 
        name: str, 
        version: str, 
        metadata: Dict[str, Any] = None,
        core_api: Optional[CoreAPI] = None
    ):
        """Initialize input plugin."""
        super().__init__(name, version, PluginType.INPUT, metadata, core_api)
    
    @abstractmethod
    async def execute(self, config: Dict[str, Any]) -> list[Dict[str, Any]]:
        """Execute the plugin to fetch papers.
        
        Args:
            config: Plugin configuration values
            
        Returns:
            List of paper data dictionaries
        """
        pass


class ProcessingPlugin(BasePlugin):
    """Base class for processing plugins (custom parsing)."""
    
    def __init__(
        self, 
        name: str, 
        version: str, 
        metadata: Dict[str, Any] = None,
        core_api: Optional[CoreAPI] = None
    ):
        """Initialize processing plugin."""
        super().__init__(name, version, PluginType.PROCESSING, metadata, core_api)
    
    @abstractmethod
    async def execute(self, paper: Paper, text: str, config: Dict[str, Any]) -> str:
        """Execute the plugin to process paper text.
        
        Args:
            paper: The paper entity
            text: Paper text to process
            config: Plugin configuration values
            
        Returns:
            Processed text
        """
        pass

