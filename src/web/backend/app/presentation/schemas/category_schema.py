"""Category API schemas."""
from pydantic import BaseModel
from uuid import UUID


class CategoryResponse(BaseModel):
    """Category response schema."""
    
    id: UUID
    name: str
    enabled: bool
    num_papers: int
    
    class Config:
        from_attributes = True


class UpdateCategoriesRequest(BaseModel):
    """Update categories request schema."""
    
    categories: list[str]

