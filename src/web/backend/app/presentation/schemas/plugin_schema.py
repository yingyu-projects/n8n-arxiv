"""Plugin API schemas."""
from pydantic import BaseModel
from typing import Dict, Any
from uuid import UUID
from datetime import datetime


class PluginResponse(BaseModel):
    """Plugin response schema."""
    
    id: UUID
    name: str
    type: str
    version: str
    config_schema: Dict[str, Any]
    enabled: bool
    metadata: Dict[str, Any]
    
    @classmethod
    def from_dto(cls, dto):
        """Create from DTO."""
        return cls(
            id=dto.id,
            name=dto.name,
            type=dto.type.value,
            version=dto.version,
            config_schema=dto.config_schema,
            enabled=dto.enabled,
            metadata=dto.metadata,
        )


class PluginConfigSchemaResponse(BaseModel):
    """Plugin configuration schema response."""
    
    schema: Dict[str, Any]


class UpdatePluginRequest(BaseModel):
    """Update plugin request schema."""
    
    enabled: bool = None

