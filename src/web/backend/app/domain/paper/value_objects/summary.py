"""Summary value object."""
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class Summary:
    """Immutable summary value object."""
    
    content: Dict[str, Any]
    
    def __post_init__(self):
        """Validate summary."""
        if not self.content:
            raise ValueError("Summary content cannot be empty")
        
        if not isinstance(self.content, dict):
            raise ValueError("Summary content must be a dictionary")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.content
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Summary":
        """Create from dictionary."""
        return cls(content=data)

