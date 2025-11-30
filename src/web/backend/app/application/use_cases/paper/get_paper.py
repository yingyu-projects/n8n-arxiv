"""Get paper use case."""
from uuid import UUID
from typing import Optional

from app.domain.paper.repositories.paper_repository import PaperRepository
from app.application.dto.paper_dto import PaperDTO


class GetPaperUseCase:
    """Use case for getting a paper by ID."""
    
    def __init__(self, paper_repository: PaperRepository):
        """Initialize use case."""
        self._paper_repository = paper_repository
    
    async def execute(self, paper_id: UUID) -> Optional[PaperDTO]:
        """Execute use case."""
        paper = await self._paper_repository.find_by_id(paper_id)
        
        if not paper:
            return None
        
        return PaperDTO.from_domain(paper)

