"""Workflow API routes."""
from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Dict, Any

from app.presentation.schemas.workflow_schema import (
    TriggerWorkflowRequest,
    WorkflowResponse,
    WorkflowStatusResponse,
)
from app.application.use_cases.workflow.trigger_parsing_workflow import (
    TriggerParsingWorkflowUseCase,
)
from app.presentation.api.dependencies import (
    get_paper_repository,
    get_config_repository,
    get_arxiv_client,
    get_pdf_client,
    get_text_cleaner,
    get_config_loader,
)
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.config.repositories.config_repository import ConfigRepository
from app.infrastructure.external.arxiv_client import ArxivClient
from app.infrastructure.external.pdf_client import PdfClient
from app.infrastructure.services.text_cleaner import TextCleaner
from app.infrastructure.services.config_loader import ConfigLoader
from app.infrastructure.services.workflow_status_manager import workflow_status_manager


router = APIRouter()


async def run_workflow_background(
    use_case: TriggerParsingWorkflowUseCase,
    categories: list[str],
    num_papers: int,
) -> None:
    """Run workflow in background."""
    await use_case.execute(
        categories=categories,
        num_papers=num_papers,
    )


@router.post("/workflow/trigger", response_model=Dict[str, str])
async def trigger_workflow(
    request: TriggerWorkflowRequest,
    background_tasks: BackgroundTasks,
    paper_repository: PaperRepository = Depends(get_paper_repository),
    config_repository: ConfigRepository = Depends(get_config_repository),
    arxiv_client: ArxivClient = Depends(get_arxiv_client),
    pdf_client: PdfClient = Depends(get_pdf_client),
    text_cleaner: TextCleaner = Depends(get_text_cleaner),
    config_loader: ConfigLoader = Depends(get_config_loader),
):
    """Trigger arXiv parsing workflow (runs in background)."""
    # Check if workflow is already running
    status = await workflow_status_manager.get_status()
    if status["status"] in ["running", "stopping"]:
        return {"message": "Workflow is already running", "status": status["status"]}
    
    use_case = TriggerParsingWorkflowUseCase(
        paper_repository=paper_repository,
        config_repository=config_repository,
        arxiv_client=arxiv_client,
        pdf_client=pdf_client,
        text_cleaner=text_cleaner,
        config_loader=config_loader,
        status_manager=workflow_status_manager,
    )
    
    # Run workflow in background
    background_tasks.add_task(
        run_workflow_background,
        use_case,
        request.categories,
        request.num_papers,
    )
    
    return {"message": "Workflow started", "status": "running"}


@router.get("/workflow/status", response_model=WorkflowStatusResponse)
async def get_workflow_status():
    """Get current workflow status."""
    status = await workflow_status_manager.get_status()
    return WorkflowStatusResponse(**status)


@router.post("/workflow/stop", response_model=Dict[str, str])
async def stop_workflow():
    """Stop the running workflow."""
    await workflow_status_manager.stop_workflow()
    return {"message": "Workflow stop requested"}

