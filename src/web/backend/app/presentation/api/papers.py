"""Paper API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import Optional

from app.presentation.schemas.paper_schema import (
    PaperResponse,
    PaperListResponse,
    PaperListQuery,
)
from app.application.use_cases.paper.get_paper import GetPaperUseCase
from app.application.use_cases.paper.list_papers import ListPapersUseCase
from app.presentation.api.dependencies import get_paper_repository
from app.domain.paper.repositories.paper_repository import PaperRepository


router = APIRouter()


@router.get("/papers", response_model=list[PaperListResponse])
async def list_papers(
    category: Optional[str] = Query(None),
    project_id: Optional[UUID] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    paper_repository: PaperRepository = Depends(get_paper_repository),
):
    """List papers with optional filtering."""
    use_case = ListPapersUseCase(paper_repository)
    papers = await use_case.execute(category=category, project_id=project_id, limit=limit, offset=offset)
    
    return [
        PaperListResponse(
            id=paper.id,
            title=paper.title,
            pdf_link=paper.pdf_link,
            category=paper.category,
            parsed_at=paper.parsed_at,
            created_at=paper.created_at,
        )
        for paper in papers
    ]


@router.get("/papers/{paper_id}", response_model=PaperResponse)
async def get_paper(
    paper_id: UUID,
    paper_repository: PaperRepository = Depends(get_paper_repository),
):
    """Get paper by ID."""
    use_case = GetPaperUseCase(paper_repository)
    paper = await use_case.execute(paper_id)
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return PaperResponse(
        id=paper.id,
        title=paper.title,
        pdf_link=paper.pdf_link,
        category=paper.category,
        arxiv_id=paper.arxiv_id,
        summary=paper.summary,
        parsed_at=paper.parsed_at,
        created_at=paper.created_at,
    )

