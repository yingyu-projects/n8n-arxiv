"""Plugin repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.plugin.entities.plugin import Plugin
from app.domain.plugin.value_objects.plugin_type import PluginType


class PluginRepository(ABC):
    """Abstract repository interface for Plugin entity."""
    
    @abstractmethod
    async def save(self, plugin: Plugin) -> Plugin:
        """Save a plugin."""
        pass
    
    @abstractmethod
    async def find_by_id(self, plugin_id: UUID) -> Optional[Plugin]:
        """Find plugin by ID."""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Plugin]:
        """Find plugin by name."""
        pass
    
    @abstractmethod
    async def find_all(
        self,
        plugin_type: Optional[PluginType] = None,
        enabled_only: bool = False,
    ) -> List[Plugin]:
        """Find all plugins with optional filtering."""
        pass

