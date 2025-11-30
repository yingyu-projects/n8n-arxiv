"""Paper DTOs."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


@dataclass
class PaperDTO:
    """Paper data transfer object."""
    
    id: UUID
    title: str
    pdf_link: str
    category: str
    arxiv_id: Optional[str]
    summary: Optional[Dict[str, Any]]
    parsed_at: Optional[datetime]
    created_at: datetime
    
    @classmethod
    def from_domain(cls, paper) -> "PaperDTO":
        """Create DTO from domain entity."""
        return cls(
            id=paper.id,
            title=paper.title,
            pdf_link=paper.get_pdf_link_str(),
            category=paper.category,
            arxiv_id=paper.get_arxiv_id_str(),
            summary=paper.summary.to_dict() if paper.summary else None,
            parsed_at=paper.parsed_at,
            created_at=paper.created_at,
        )


@dataclass
class PaperListDTO:
    """Paper list item DTO."""
    
    id: UUID
    title: str
    pdf_link: str
    category: str
    parsed_at: Optional[datetime]
    created_at: datetime
    
    @classmethod
    def from_domain(cls, paper) -> "PaperListDTO":
        """Create DTO from domain entity."""
        return cls(
            id=paper.id,
            title=paper.title,
            pdf_link=paper.get_pdf_link_str(),
            category=paper.category,
            parsed_at=paper.parsed_at,
            created_at=paper.created_at,
        )

