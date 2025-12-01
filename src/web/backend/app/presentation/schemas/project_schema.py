"""Project API schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class CreateProjectRequest(BaseModel):
    """Create project request schema."""
    
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    """Update project request schema."""
    
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    """Project entity response schema."""
    
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dto(cls, dto):
        """Create from DTO."""
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

