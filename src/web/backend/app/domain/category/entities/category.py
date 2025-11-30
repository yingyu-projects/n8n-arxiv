"""Category domain entity."""
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Category:
    """Category domain entity."""
    
    id: UUID
    name: str
    enabled: bool
    num_papers: int
    
    def __post_init__(self):
        """Validate entity."""
        if not self.name:
            raise ValueError("Category name cannot be empty")
    
    @classmethod
    def create(cls, name: str, enabled: bool = True) -> "Category":
        """Factory method to create a new category."""
        return cls(
            id=uuid4(),
            name=name,
            enabled=enabled,
            num_papers=0,
        )
    
    def enable(self) -> None:
        """Enable category."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable category."""
        self.enabled = False

