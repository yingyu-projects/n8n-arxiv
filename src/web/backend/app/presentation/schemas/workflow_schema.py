"""Workflow API schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime


class TriggerWorkflowRequest(BaseModel):
    """Trigger workflow request schema."""
    
    categories: List[str] = Field(..., min_items=1)
    num_papers: int = Field(default=50, ge=1, le=100)


class WorkflowExecutionResponse(BaseModel):
    """Workflow execution response schema."""
    
    processed: int
    skipped: int
    errors: List[str]
    papers: List[Dict[str, Any]]


class WorkflowStatusResponse(BaseModel):
    """Workflow status response schema."""
    
    status: str
    total_papers: int
    processed: int
    skipped: int
    errors: List[str]
    papers: List[Dict[str, Any]]
    elapsed_time: Optional[float] = None


# New workflow management schemas
class CreateWorkflowRequest(BaseModel):
    """Create workflow request schema."""
    
    name: str = Field(..., min_length=1)
    categories: List[str] = Field(..., min_items=1)
    num_papers: int = Field(default=50, ge=1, le=100)
    description: Optional[str] = None


class UpdateWorkflowRequest(BaseModel):
    """Update workflow request schema."""
    
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    categories: Optional[List[str]] = Field(None, min_items=1)
    num_papers: Optional[int] = Field(None, ge=1, le=100)
    enabled: Optional[bool] = None


class WorkflowResponse(BaseModel):
    """Workflow entity response schema."""
    
    id: UUID
    name: str
    description: Optional[str]
    categories: List[str]
    num_papers: int
    enabled: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dto(cls, dto):
        """Create from DTO."""
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            categories=dto.categories,
            num_papers=dto.num_papers,
            enabled=dto.enabled,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class PluginConfigSchema(BaseModel):
    """Plugin configuration schema."""
    
    plugin_id: UUID
    enabled: bool
    config: Dict[str, Any]


class UpdateWorkflowConfigRequest(BaseModel):
    """Update workflow configuration request schema."""
    
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    categories: Optional[List[str]] = Field(None, min_items=1)
    num_papers: Optional[int] = Field(None, ge=1, le=100)
    enabled: Optional[bool] = None
    plugin_configs: Optional[List[PluginConfigSchema]] = None


class WorkflowConfigResponse(BaseModel):
    """Workflow configuration response schema."""
    
    class PluginConfig(BaseModel):
        """Plugin config in workflow config."""
        
        id: UUID
        plugin_id: UUID
        enabled: bool
        config: Dict[str, Any]
        
        @classmethod
        def from_dto(cls, dto):
            """Create from DTO."""
            return cls(
                id=dto.id,
                plugin_id=dto.plugin_id,
                enabled=dto.enabled,
                config=dto.config,
            )
    
    workflow: WorkflowResponse
    plugin_configs: List[PluginConfig]

