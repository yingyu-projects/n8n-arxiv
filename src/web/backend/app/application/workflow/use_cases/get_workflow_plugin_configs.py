"""Get workflow plugin configs use case."""
from typing import List
from uuid import UUID

from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository
from app.application.dto.workflow_plugin_config_dto import WorkflowPluginConfigDTO


class GetWorkflowPluginConfigsUseCase:
    """Use case for getting workflow plugin configurations."""
    
    def __init__(self, workflow_plugin_config_repository: WorkflowPluginConfigRepository):
        """Initialize use case."""
        self._workflow_plugin_config_repository = workflow_plugin_config_repository
    
    async def execute(self, workflow_id: UUID) -> List[WorkflowPluginConfigDTO]:
        """Execute use case - get workflow plugin configs.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            List of WorkflowPluginConfigDTO
        """
        configs = await self._workflow_plugin_config_repository.find_by_workflow_id(workflow_id)
        return [WorkflowPluginConfigDTO.from_domain(config) for config in configs]

