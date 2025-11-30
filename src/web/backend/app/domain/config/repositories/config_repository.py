"""Config repository interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.config.entities.config import Config


class ConfigRepository(ABC):
    """Abstract repository interface for Config entity."""
    
    @abstractmethod
    async def save(self, config: Config) -> Config:
        """Save a config."""
        pass
    
    @abstractmethod
    async def find_by_id(self, config_id: UUID) -> Optional[Config]:
        """Find config by ID."""
        pass
    
    @abstractmethod
    async def find_by_key(self, key: str) -> Optional[Config]:
        """Find config by key."""
        pass

