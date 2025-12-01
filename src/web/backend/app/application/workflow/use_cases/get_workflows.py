"""Get workflows use case."""
from typing import List

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.application.dto.workflow_dto import WorkflowDTO


class GetWorkflowsUseCase:
    """Use case for getting workflows."""
    
    def __init__(self, workflow_repository: WorkflowRepository):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
    
    async def execute(self, enabled_only: bool = False) -> List[WorkflowDTO]:
        """Execute use case - get workflows.
        
        Args:
            enabled_only: Only return enabled workflows
            
        Returns:
            List of WorkflowDTO
        """
        workflows = await self._workflow_repository.find_all(enabled_only=enabled_only)
        return [WorkflowDTO.from_domain(workflow) for workflow in workflows]

