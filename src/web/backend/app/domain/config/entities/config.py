"""Config domain entity."""
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Config:
    """Config domain entity."""
    
    id: UUID
    key: str
    value: str
    
    def __post_init__(self):
        """Validate entity."""
        if not self.key:
            raise ValueError("Config key cannot be empty")
        if self.value is None:
            raise ValueError("Config value cannot be None")
    
    @classmethod
    def create(cls, key: str, value: str) -> "Config":
        """Factory method to create a new config."""
        return cls(
            id=uuid4(),
            key=key,
            value=value,
        )
    
    def update_value(self, value: str) -> None:
        """Update config value."""
        if value is None:
            raise ValueError("Config value cannot be None")
        self.value = value

