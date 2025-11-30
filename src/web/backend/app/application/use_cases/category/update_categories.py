"""Update categories use case."""
from typing import List
from app.domain.category.repositories.category_repository import CategoryRepository
from app.domain.category.entities.category import Category
from app.application.dto.category_dto import CategoryDTO


class UpdateCategoriesUseCase:
    """Use case for updating categories."""
    
    def __init__(self, category_repository: CategoryRepository):
        """Initialize use case."""
        self._category_repository = category_repository
    
    async def execute(self, category_names: List[str]) -> List[CategoryDTO]:
        """Execute use case - creates or updates categories."""
        result = []
        
        for name in category_names:
            existing = await self._category_repository.find_by_name(name)
            
            if existing:
                existing.enable()
                category = await self._category_repository.save(existing)
            else:
                new_category = Category.create(name=name, enabled=True)
                category = await self._category_repository.save(new_category)
            
            result.append(CategoryDTO.from_domain(category))
        
        return result

