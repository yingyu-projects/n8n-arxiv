"""Remove plugin from workflow use case."""
from uuid import UUID

from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository


class RemovePluginFromWorkflowUseCase:
    """Use case for removing a plugin from a workflow."""
    
    def __init__(self, workflow_plugin_config_repository: WorkflowPluginConfigRepository):
        """Initialize use case."""
        self._workflow_plugin_config_repository = workflow_plugin_config_repository
    
    async def execute(
        self,
        workflow_id: UUID,
        plugin_id: UUID,
    ) -> None:
        """Execute use case - remove plugin from workflow.
        
        Args:
            workflow_id: Workflow ID
            plugin_id: Plugin ID
        """
        await self._workflow_plugin_config_repository.delete_by_workflow_and_plugin(
            workflow_id, plugin_id
        )

