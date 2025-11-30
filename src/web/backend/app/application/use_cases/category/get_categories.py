"""Get categories use case."""
from typing import List
from app.domain.category.repositories.category_repository import CategoryRepository
from app.application.dto.category_dto import CategoryDTO


class GetCategoriesUseCase:
    """Use case for getting categories."""
    
    def __init__(self, category_repository: CategoryRepository):
        """Initialize use case."""
        self._category_repository = category_repository
    
    async def execute(self, enabled_only: bool = False) -> List[CategoryDTO]:
        """Execute use case."""
        categories = await self._category_repository.find_all(enabled_only=enabled_only)
        return [CategoryDTO.from_domain(cat) for cat in categories]

