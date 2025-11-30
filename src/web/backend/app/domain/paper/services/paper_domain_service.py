"""Paper domain service."""
from typing import Optional
from app.domain.paper.entities.paper import Paper
from app.domain.paper.repositories.paper_repository import PaperRepository


class PaperDomainService:
    """Domain service for paper-related business logic."""
    
    def __init__(self, paper_repository: PaperRepository):
        """Initialize with repository."""
        self._paper_repository = paper_repository
    
    async def ensure_paper_not_duplicate(self, pdf_link: str) -> bool:
        """Check if paper already exists by PDF link."""
        existing = await self._paper_repository.find_by_pdf_link(pdf_link)
        return existing is None
    
    async def get_or_create_paper(
        self,
        title: str,
        pdf_link: str,
        category: str,
        arxiv_id: Optional[str] = None,
    ) -> tuple[Paper, bool]:
        """Get existing paper or create new one. Returns (paper, is_new)."""
        existing = await self._paper_repository.find_by_pdf_link(pdf_link)
        
        if existing:
            return existing, False
        
        new_paper = Paper.create(
            title=title,
            pdf_link=pdf_link,
            category=category,
            arxiv_id=arxiv_id,
        )
        
        return new_paper, True

