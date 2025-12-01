"""Get workflows use case."""
from typing import List, Optional
from uuid import UUID

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.application.dto.workflow_dto import WorkflowDTO


class GetWorkflowsUseCase:
    """Use case for getting workflows."""
    
    def __init__(self, workflow_repository: WorkflowRepository):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
    
    async def execute(self, enabled_only: bool = False, project_id: Optional[UUID] = None) -> List[WorkflowDTO]:
        """Execute use case - get workflows.
        
        Args:
            enabled_only: Only return enabled workflows
            project_id: Optional project ID to filter by
            
        Returns:
            List of WorkflowDTO
        """
        workflows = await self._workflow_repository.find_all(enabled_only=enabled_only, project_id=project_id)
        return [WorkflowDTO.from_domain(workflow) for workflow in workflows]

