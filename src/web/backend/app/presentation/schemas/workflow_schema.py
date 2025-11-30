"""Workflow API schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class TriggerWorkflowRequest(BaseModel):
    """Trigger workflow request schema."""
    
    categories: List[str] = Field(..., min_items=1)
    num_papers: int = Field(default=50, ge=1, le=100)


class WorkflowResponse(BaseModel):
    """Workflow response schema."""
    
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

