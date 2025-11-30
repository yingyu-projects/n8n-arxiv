"""Config DTOs."""
from dataclasses import dataclass
from uuid import UUID


@dataclass
class ConfigDTO:
    """Config data transfer object."""
    
    id: UUID
    key: str
    value: str
    
    @classmethod
    def from_domain(cls, config) -> "ConfigDTO":
        """Create DTO from domain entity."""
        return cls(
            id=config.id,
            key=config.key,
            value=config.value,
        )

