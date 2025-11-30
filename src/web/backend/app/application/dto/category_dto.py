"""Category DTOs."""
from dataclasses import dataclass
from uuid import UUID


@dataclass
class CategoryDTO:
    """Category data transfer object."""
    
    id: UUID
    name: str
    enabled: bool
    num_papers: int
    
    @classmethod
    def from_domain(cls, category) -> "CategoryDTO":
        """Create DTO from domain entity."""
        return cls(
            id=category.id,
            name=category.name,
            enabled=category.enabled,
            num_papers=category.num_papers,
        )

