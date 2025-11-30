"""Workflow API schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class TriggerWorkflowRequest(BaseModel):
    """Trigger workflow request schema."""
    
    categories: List[str] = Field(..., min_items=1)
    num_papers: int = Field(default=50, ge=1, le=100)
    summarize_prompt: str = Field(default="")


class WorkflowResponse(BaseModel):
    """Workflow response schema."""
    
    processed: int
    skipped: int
    errors: List[str]
    papers: List[Dict[str, Any]]

