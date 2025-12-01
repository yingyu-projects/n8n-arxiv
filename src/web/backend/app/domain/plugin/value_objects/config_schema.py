"""Config schema value object."""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class ConfigSchema:
    """Immutable config schema value object."""
    
    schema: Dict[str, Any]
    
    def __post_init__(self):
        """Validate config schema."""
        if not isinstance(self.schema, dict):
            raise ValueError("Config schema must be a dictionary")
        if "type" not in self.schema:
            raise ValueError("Config schema must have a 'type' field")
        if self.schema["type"] != "object":
            raise ValueError("Config schema type must be 'object'")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.schema
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigSchema":
        """Create from dictionary."""
        return cls(schema=data)

