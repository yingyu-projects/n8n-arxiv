"""Check paper exists use case."""
from app.domain.paper.repositories.paper_repository import PaperRepository


class CheckPaperExistsUseCase:
    """Use case for checking if a paper exists by PDF link."""
    
    def __init__(self, paper_repository: PaperRepository):
        """Initialize use case."""
        self._paper_repository = paper_repository
    
    async def execute(self, pdf_link: str) -> bool:
        """Execute use case."""
        return await self._paper_repository.exists_by_pdf_link(pdf_link)

