"""Workflow DTO."""
from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.domain.workflow.entities.workflow import Workflow


@dataclass
class WorkflowDTO:
    """Data transfer object for Workflow."""
    
    id: UUID
    name: str
    description: Optional[str]
    categories: List[str]
    num_papers: int
    enabled: bool
    project_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, workflow: Workflow) -> "WorkflowDTO":
        """Create DTO from domain entity."""
        return cls(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            categories=workflow.categories,
            num_papers=workflow.num_papers,
            enabled=workflow.enabled,
            project_id=workflow.project_id,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at,
        )

