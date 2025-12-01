"""Add plugin to workflow use case."""
from typing import Dict, Any
from uuid import UUID

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.workflow.entities.workflow_plugin_config import WorkflowPluginConfig
from app.application.dto.workflow_plugin_config_dto import WorkflowPluginConfigDTO


class AddPluginToWorkflowUseCase:
    """Use case for adding a plugin to a workflow."""
    
    def __init__(
        self,
        workflow_repository: WorkflowRepository,
        workflow_plugin_config_repository: WorkflowPluginConfigRepository,
        plugin_repository: PluginRepository,
    ):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
        self._workflow_plugin_config_repository = workflow_plugin_config_repository
        self._plugin_repository = plugin_repository
    
    async def execute(
        self,
        workflow_id: UUID,
        plugin_id: UUID,
        config: Dict[str, Any] = None,
        enabled: bool = True,
    ) -> WorkflowPluginConfigDTO:
        """Execute use case - add plugin to workflow.
        
        Args:
            workflow_id: Workflow ID
            plugin_id: Plugin ID
            config: Optional plugin configuration
            enabled: Whether plugin is enabled
            
        Returns:
            WorkflowPluginConfigDTO
        """
        # Verify workflow exists
        workflow = await self._workflow_repository.find_by_id(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")
        
        # Verify plugin exists
        plugin = await self._plugin_repository.find_by_id(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin with ID {plugin_id} not found")
        
        # Check if plugin is already added to workflow
        existing = await self._workflow_plugin_config_repository.find_by_workflow_and_plugin(
            workflow_id, plugin_id
        )
        
        if existing:
            # Update existing config
            existing.update_config(config or {})
            if enabled:
                existing.enable()
            else:
                existing.disable()
            config_entity = await self._workflow_plugin_config_repository.save(existing)
        else:
            # Create new config
            config_entity = WorkflowPluginConfig.create(
                workflow_id=workflow_id,
                plugin_id=plugin_id,
                enabled=enabled,
                config=config or {},
            )
            config_entity = await self._workflow_plugin_config_repository.save(config_entity)
        
        return WorkflowPluginConfigDTO.from_domain(config_entity)

