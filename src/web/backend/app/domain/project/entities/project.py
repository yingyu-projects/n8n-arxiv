"""Project domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Project:
    """Project domain entity with business logic."""
    
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate entity."""
        if not self.name:
            raise ValueError("Project name cannot be empty")
    
    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str] = None,
    ) -> "Project":
        """Factory method to create a new project."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
        )
    
    def update_name(self, name: str) -> None:
        """Update project name."""
        if not name:
            raise ValueError("Project name cannot be empty")
        self.name = name
        self.updated_at = datetime.utcnow()
    
    def update_description(self, description: Optional[str]) -> None:
        """Update project description."""
        self.description = description
        self.updated_at = datetime.utcnow()


