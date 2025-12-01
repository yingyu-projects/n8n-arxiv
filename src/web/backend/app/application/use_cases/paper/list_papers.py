"""List papers use case."""
from typing import List, Optional
from uuid import UUID

from app.domain.paper.repositories.paper_repository import PaperRepository
from app.application.dto.paper_dto import PaperListDTO


class ListPapersUseCase:
    """Use case for listing papers."""
    
    def __init__(self, paper_repository: PaperRepository):
        """Initialize use case."""
        self._paper_repository = paper_repository
    
    async def execute(
        self,
        category: Optional[str] = None,
        project_id: Optional[UUID] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[PaperListDTO]:
        """Execute use case."""
        papers = await self._paper_repository.find_all(
            category=category,
            project_id=project_id,
            limit=limit,
            offset=offset,
        )
        
        return [PaperListDTO.from_domain(paper) for paper in papers]

