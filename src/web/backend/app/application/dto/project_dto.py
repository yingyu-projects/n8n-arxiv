"""Project DTO."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.domain.project.entities.project import Project


@dataclass
class ProjectDTO:
    """Data transfer object for Project."""
    
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, project: Project) -> "ProjectDTO":
        """Create DTO from domain entity."""
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

