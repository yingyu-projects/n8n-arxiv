"""Workflow API routes."""
from fastapi import APIRouter, Depends

from app.presentation.schemas.workflow_schema import (
    TriggerWorkflowRequest,
    WorkflowResponse,
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


router = APIRouter()


@router.post("/workflow/trigger", response_model=WorkflowResponse)
async def trigger_workflow(
    request: TriggerWorkflowRequest,
    paper_repository: PaperRepository = Depends(get_paper_repository),
    config_repository: ConfigRepository = Depends(get_config_repository),
    arxiv_client: ArxivClient = Depends(get_arxiv_client),
    pdf_client: PdfClient = Depends(get_pdf_client),
    text_cleaner: TextCleaner = Depends(get_text_cleaner),
    config_loader: ConfigLoader = Depends(get_config_loader),
):
    """Trigger arXiv parsing workflow."""
    use_case = TriggerParsingWorkflowUseCase(
        paper_repository=paper_repository,
        config_repository=config_repository,
        arxiv_client=arxiv_client,
        pdf_client=pdf_client,
        text_cleaner=text_cleaner,
        config_loader=config_loader,
    )
    
    result = await use_case.execute(
        categories=request.categories,
        num_papers=request.num_papers,
        summarize_prompt=request.summarize_prompt,
    )
    
    return WorkflowResponse(
        processed=result["processed"],
        skipped=result["skipped"],
        errors=result["errors"],
        papers=result["papers"],
    )

