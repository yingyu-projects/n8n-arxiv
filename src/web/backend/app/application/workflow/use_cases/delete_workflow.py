"""Delete workflow use case."""
from uuid import UUID

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository


class DeleteWorkflowUseCase:
    """Use case for deleting a workflow."""
    
    def __init__(self, workflow_repository: WorkflowRepository):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
    
    async def execute(self, workflow_id: UUID) -> None:
        """Execute use case - delete workflow.
        
        Args:
            workflow_id: Workflow ID
        """
        workflow = await self._workflow_repository.find_by_id(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")
        
        await self._workflow_repository.delete(workflow_id)

