"""Plugin executor for executing plugins asynchronously."""
import asyncio
from typing import Dict, Any, Optional
from uuid import UUID

from app.domain.paper.entities.paper import Paper
from app.domain.plugin.entities.plugin_execution import PluginExecution
from app.domain.plugin.repositories.plugin_execution_repository import PluginExecutionRepository
from app.domain.plugin.value_objects.plugin_status import PluginStatus
from app.application.plugin.plugin_registry import PluginRegistry
from app.infrastructure.plugin.base_plugin import OutputPlugin


class PluginExecutor:
    """Executor for running plugins asynchronously."""
    
    def __init__(
        self,
        plugin_registry: PluginRegistry,
        execution_repository: PluginExecutionRepository,
    ):
        """Initialize plugin executor.
        
        Args:
            plugin_registry: Plugin registry for getting plugin instances
            execution_repository: Repository for execution tracking
        """
        self._plugin_registry = plugin_registry
        self._execution_repository = execution_repository
    
    async def execute_output_plugin(
        self,
        plugin_id: UUID,
        plugin_instance: Any,
        paper: Paper,
        config: Dict[str, Any],
        workflow_id: UUID,
        workflow_run_id: str,
    ) -> PluginExecution:
        """Execute an output plugin.
        
        Args:
            plugin_id: Plugin ID
            plugin_instance: Plugin instance (OutputPlugin)
            paper: Paper to process
            config: Plugin configuration
            workflow_id: Workflow ID
            workflow_run_id: Workflow run identifier
            
        Returns:
            PluginExecution entity
        """
        # Create execution record
        execution = PluginExecution.create(
            plugin_id=plugin_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            paper_id=paper.id,
            config=config,
        )
        execution = await self._execution_repository.save(execution)
        
        # Execute plugin asynchronously (fire and forget)
        # Note: This runs in the background and doesn't block workflow execution
        try:
            asyncio.create_task(self._execute_plugin_async(execution, plugin_instance, paper))
        except Exception as e:
            # If task creation fails, mark execution as failed
            execution.mark_failed(f"Failed to create execution task: {str(e)}")
            await self._execution_repository.save(execution)
        
        return execution
    
    async def _execute_plugin_async(
        self,
        execution: PluginExecution,
        plugin_instance: OutputPlugin,
        paper: Paper,
    ) -> None:
        """Execute plugin asynchronously and update execution status.
        
        Args:
            execution: Execution entity
            plugin_instance: Plugin instance
            paper: Paper to process
        """
        try:
            execution.mark_running()
            await self._execution_repository.save(execution)
            
            # Execute plugin
            result = await plugin_instance.execute(paper, execution.config)
            
            # Mark as successful
            execution.mark_success(result)
            await self._execution_repository.save(execution)
        
        except Exception as e:
            # Mark as failed
            execution.mark_failed(str(e))
            await self._execution_repository.save(execution)

