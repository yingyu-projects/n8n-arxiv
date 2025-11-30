"""Category API routes."""
from fastapi import APIRouter, Depends, Query
from typing import List

from app.presentation.schemas.category_schema import (
    CategoryResponse,
    UpdateCategoriesRequest,
)
from app.application.use_cases.category.get_categories import GetCategoriesUseCase
from app.application.use_cases.category.update_categories import UpdateCategoriesUseCase
from app.presentation.api.dependencies import get_category_repository
from app.domain.category.repositories.category_repository import CategoryRepository


router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    enabled_only: bool = Query(False),
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    """Get categories."""
    use_case = GetCategoriesUseCase(category_repository)
    categories = await use_case.execute(enabled_only=enabled_only)
    
    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            enabled=cat.enabled,
            num_papers=cat.num_papers,
        )
        for cat in categories
    ]


@router.post("/categories", response_model=List[CategoryResponse])
async def update_categories(
    request: UpdateCategoriesRequest,
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    """Update categories."""
    use_case = UpdateCategoriesUseCase(category_repository)
    categories = await use_case.execute(request.categories)
    
    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            enabled=cat.enabled,
            num_papers=cat.num_papers,
        )
        for cat in categories
    ]

