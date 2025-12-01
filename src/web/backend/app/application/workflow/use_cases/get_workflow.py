"""Get workflow use case."""
from typing import Optional
from uuid import UUID

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.application.dto.workflow_dto import WorkflowDTO


class GetWorkflowUseCase:
    """Use case for getting a workflow."""
    
    def __init__(self, workflow_repository: WorkflowRepository):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
    
    async def execute(self, workflow_id: UUID) -> Optional[WorkflowDTO]:
        """Execute use case - get workflow.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            WorkflowDTO or None if not found
        """
        workflow = await self._workflow_repository.find_by_id(workflow_id)
        return WorkflowDTO.from_domain(workflow) if workflow else None

