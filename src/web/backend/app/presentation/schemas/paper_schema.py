"""Paper API schemas."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class PaperResponse(BaseModel):
    """Paper response schema."""
    
    id: UUID
    title: str
    pdf_link: str
    category: str
    arxiv_id: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    parsed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaperListResponse(BaseModel):
    """Paper list item response schema."""
    
    id: UUID
    title: str
    pdf_link: str
    category: str
    parsed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaperListQuery(BaseModel):
    """Paper list query parameters."""
    
    category: Optional[str] = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

