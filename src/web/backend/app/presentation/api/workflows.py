"""Workflows API routes."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from uuid import UUID

from app.presentation.schemas.workflow_schema import (
    CreateWorkflowRequest,
    UpdateWorkflowRequest,
    WorkflowResponse,
    WorkflowConfigResponse,
    UpdateWorkflowConfigRequest,
)
from app.application.workflow.use_cases.create_workflow import CreateWorkflowUseCase
from app.application.workflow.use_cases.get_workflows import GetWorkflowsUseCase
from app.application.workflow.use_cases.get_workflow import GetWorkflowUseCase
from app.application.workflow.use_cases.update_workflow import UpdateWorkflowUseCase
from app.application.workflow.use_cases.delete_workflow import DeleteWorkflowUseCase
from app.application.workflow.use_cases.add_plugin_to_workflow import AddPluginToWorkflowUseCase
from app.application.workflow.use_cases.remove_plugin_from_workflow import RemovePluginFromWorkflowUseCase
from app.application.workflow.use_cases.get_workflow_plugin_configs import GetWorkflowPluginConfigsUseCase
from app.presentation.api.dependencies import (
    get_workflow_repository,
    get_workflow_plugin_config_repository,
    get_plugin_repository,
)
from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.application.use_cases.workflow.trigger_parsing_workflow import TriggerParsingWorkflowUseCase
from app.presentation.api.dependencies import (
    get_paper_repository,
    get_config_repository,
    get_arxiv_client,
    get_pdf_client,
    get_text_cleaner,
    get_config_loader,
    get_plugin_registry,
    get_plugin_executor,
)
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.config.repositories.config_repository import ConfigRepository
from app.infrastructure.external.arxiv_client import ArxivClient
from app.infrastructure.external.pdf_client import PdfClient
from app.infrastructure.services.text_cleaner import TextCleaner
from app.infrastructure.services.config_loader import ConfigLoader
from app.application.plugin.plugin_registry import PluginRegistry
from app.application.plugin.plugin_executor import PluginExecutor
from app.infrastructure.services.workflow_status_manager import workflow_status_manager


router = APIRouter()


@router.get("/workflows", response_model=List[WorkflowResponse])
async def list_workflows(
    enabled_only: bool = False,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
):
    """List all workflows."""
    use_case = GetWorkflowsUseCase(workflow_repository)
    workflows = await use_case.execute(enabled_only=enabled_only)
    return [WorkflowResponse.from_dto(w) for w in workflows]


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: UUID,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
):
    """Get workflow by ID."""
    use_case = GetWorkflowUseCase(workflow_repository)
    workflow = await use_case.execute(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
    
    return WorkflowResponse.from_dto(workflow)


@router.post("/workflows", response_model=WorkflowResponse)
async def create_workflow(
    request: CreateWorkflowRequest,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
):
    """Create a new workflow."""
    use_case = CreateWorkflowUseCase(workflow_repository)
    try:
        workflow = await use_case.execute(
            name=request.name,
            categories=request.categories,
            num_papers=request.num_papers,
            description=request.description,
        )
        return WorkflowResponse.from_dto(workflow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: UUID,
    request: UpdateWorkflowRequest,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
):
    """Update a workflow."""
    use_case = UpdateWorkflowUseCase(workflow_repository)
    try:
        workflow = await use_case.execute(
            workflow_id=workflow_id,
            name=request.name,
            description=request.description,
            categories=request.categories,
            num_papers=request.num_papers,
            enabled=request.enabled,
        )
        return WorkflowResponse.from_dto(workflow)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/workflows/{workflow_id}", response_model=Dict[str, str])
async def delete_workflow(
    workflow_id: UUID,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
):
    """Delete a workflow."""
    use_case = DeleteWorkflowUseCase(workflow_repository)
    try:
        await use_case.execute(workflow_id)
        return {"message": "Workflow deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/workflows/{workflow_id}/config", response_model=WorkflowConfigResponse)
async def get_workflow_config(
    workflow_id: UUID,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
    workflow_plugin_config_repository: WorkflowPluginConfigRepository = Depends(get_workflow_plugin_config_repository),
):
    """Get workflow configuration including plugin configs."""
    workflow_use_case = GetWorkflowUseCase(workflow_repository)
    workflow = await workflow_use_case.execute(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow with ID {workflow_id} not found")
    
    plugin_configs_use_case = GetWorkflowPluginConfigsUseCase(workflow_plugin_config_repository)
    plugin_configs = await plugin_configs_use_case.execute(workflow_id)
    
    return WorkflowConfigResponse(
        workflow=WorkflowResponse.from_dto(workflow),
        plugin_configs=[WorkflowConfigResponse.PluginConfig.from_dto(pc) for pc in plugin_configs],
    )


@router.put("/workflows/{workflow_id}/config", response_model=WorkflowConfigResponse)
async def update_workflow_config(
    workflow_id: UUID,
    request: UpdateWorkflowConfigRequest,
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
    workflow_plugin_config_repository: WorkflowPluginConfigRepository = Depends(get_workflow_plugin_config_repository),
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
):
    """Update workflow configuration including plugin configs."""
    # Update workflow basic settings
    if request.name or request.description or request.categories or request.num_papers is not None or request.enabled is not None:
        update_use_case = UpdateWorkflowUseCase(workflow_repository)
        await update_use_case.execute(
            workflow_id=workflow_id,
            name=request.name,
            description=request.description,
            categories=request.categories,
            num_papers=request.num_papers,
            enabled=request.enabled,
        )
    
    # Update plugin configs
    if request.plugin_configs:
        add_plugin_use_case = AddPluginToWorkflowUseCase(
            workflow_repository,
            workflow_plugin_config_repository,
            plugin_repository,
        )
        remove_plugin_use_case = RemovePluginFromWorkflowUseCase(workflow_plugin_config_repository)
        
        for plugin_config in request.plugin_configs:
            if plugin_config.enabled is False:
                # Remove plugin
                await remove_plugin_use_case.execute(workflow_id, plugin_config.plugin_id)
            else:
                # Add or update plugin
                await add_plugin_use_case.execute(
                    workflow_id=workflow_id,
                    plugin_id=plugin_config.plugin_id,
                    config=plugin_config.config,
                    enabled=plugin_config.enabled,
                )
    
    # Return updated config
    return await get_workflow_config(workflow_id, workflow_repository, workflow_plugin_config_repository)


@router.post("/workflows/{workflow_id}/plugins", response_model=Dict[str, str])
async def add_plugin_to_workflow(
    workflow_id: UUID,
    request: Dict[str, Any],
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
    workflow_plugin_config_repository: WorkflowPluginConfigRepository = Depends(get_workflow_plugin_config_repository),
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
):
    """Add a plugin to a workflow."""
    # Extract plugin_id and config from request body
    if "plugin_id" not in request:
        raise HTTPException(status_code=400, detail="plugin_id is required")
    
    plugin_id = UUID(request["plugin_id"])
    config = request.get("config", {})
    enabled = request.get("enabled", True)
    
    use_case = AddPluginToWorkflowUseCase(
        workflow_repository,
        workflow_plugin_config_repository,
        plugin_repository,
    )
    try:
        await use_case.execute(workflow_id, plugin_id, config, enabled)
        return {"message": "Plugin added to workflow successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/workflows/{workflow_id}/plugins/{plugin_id}", response_model=Dict[str, str])
async def remove_plugin_from_workflow(
    workflow_id: UUID,
    plugin_id: UUID,
    workflow_plugin_config_repository: WorkflowPluginConfigRepository = Depends(get_workflow_plugin_config_repository),
):
    """Remove a plugin from a workflow."""
    use_case = RemovePluginFromWorkflowUseCase(workflow_plugin_config_repository)
    await use_case.execute(workflow_id, plugin_id)
    return {"message": "Plugin removed from workflow successfully"}


async def run_workflow_background(
    use_case: TriggerParsingWorkflowUseCase,
    workflow_id: UUID,
) -> None:
    """Run workflow in background."""
    await use_case.execute(workflow_id=workflow_id)


@router.post("/workflows/{workflow_id}/trigger", response_model=Dict[str, str])
async def trigger_workflow(
    workflow_id: UUID,
    background_tasks: BackgroundTasks,
    paper_repository: PaperRepository = Depends(get_paper_repository),
    config_repository: ConfigRepository = Depends(get_config_repository),
    workflow_repository: WorkflowRepository = Depends(get_workflow_repository),
    workflow_plugin_config_repository: WorkflowPluginConfigRepository = Depends(get_workflow_plugin_config_repository),
    arxiv_client: ArxivClient = Depends(get_arxiv_client),
    pdf_client: PdfClient = Depends(get_pdf_client),
    text_cleaner: TextCleaner = Depends(get_text_cleaner),
    config_loader: ConfigLoader = Depends(get_config_loader),
    plugin_registry: PluginRegistry = Depends(get_plugin_registry),
    plugin_executor: PluginExecutor = Depends(get_plugin_executor),
):
    """Trigger workflow execution."""
    # Check if workflow is already running
    status = await workflow_status_manager.get_status()
    if status["status"] in ["running", "stopping"]:
        return {"message": "Workflow is already running", "status": status["status"]}
    
    use_case = TriggerParsingWorkflowUseCase(
        paper_repository=paper_repository,
        config_repository=config_repository,
        workflow_repository=workflow_repository,
        workflow_plugin_config_repository=workflow_plugin_config_repository,
        arxiv_client=arxiv_client,
        pdf_client=pdf_client,
        text_cleaner=text_cleaner,
        config_loader=config_loader,
        status_manager=workflow_status_manager,
        plugin_registry=plugin_registry,
        plugin_executor=plugin_executor,
    )
    
    # Run workflow in background
    background_tasks.add_task(
        run_workflow_background,
        use_case,
        workflow_id,
    )
    
    return {"message": "Workflow started", "status": "running"}

