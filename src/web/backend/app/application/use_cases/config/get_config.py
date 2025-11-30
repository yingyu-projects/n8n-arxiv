"""Get config use case."""
from typing import Optional
from app.domain.config.repositories.config_repository import ConfigRepository
from app.application.dto.config_dto import ConfigDTO


class GetConfigUseCase:
    """Use case for getting config by key."""
    
    def __init__(self, config_repository: ConfigRepository):
        """Initialize use case."""
        self._config_repository = config_repository
    
    async def execute(self, key: str) -> Optional[ConfigDTO]:
        """Execute use case."""
        config = await self._config_repository.find_by_key(key)
        return ConfigDTO.from_domain(config) if config else None

