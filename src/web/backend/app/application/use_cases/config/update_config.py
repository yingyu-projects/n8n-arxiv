"""Update config use case."""
from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.config.entities.config import Config
from app.application.dto.config_dto import ConfigDTO


class UpdateConfigUseCase:
    """Use case for updating config."""
    
    def __init__(self, config_repository: ConfigRepository):
        """Initialize use case."""
        self._config_repository = config_repository
    
    async def execute(self, key: str, value: str) -> ConfigDTO:
        """Execute use case - creates or updates config."""
        existing = await self._config_repository.find_by_key(key)
        
        if existing:
            existing.update_value(value)
            config = await self._config_repository.save(existing)
        else:
            new_config = Config.create(key=key, value=value)
            config = await self._config_repository.save(new_config)
        
        return ConfigDTO.from_domain(config)

