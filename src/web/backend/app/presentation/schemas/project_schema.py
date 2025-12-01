"""Project API schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
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


class ProjectPluginConfigResponse(BaseModel):
    """Project plugin config response schema."""
    
    id: UUID
    project_id: UUID
    plugin_id: UUID
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dto(cls, dto):
        """Create from DTO."""
        return cls(
            id=dto.id,
            project_id=dto.project_id,
            plugin_id=dto.plugin_id,
            config=dto.config,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class UpdateProjectPluginConfigRequest(BaseModel):
    """Update project plugin config request schema."""
    
    config: Dict[str, Any] = Field(..., description="Plugin configuration values")

