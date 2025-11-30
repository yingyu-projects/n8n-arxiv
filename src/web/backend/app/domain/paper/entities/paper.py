"""Paper domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.paper.value_objects.pdf_link import PdfLink
from app.domain.paper.value_objects.arxiv_id import ArxivId
from app.domain.paper.value_objects.summary import Summary


@dataclass
class Paper:
    """Paper domain entity with business logic."""
    
    id: UUID
    title: str
    pdf_link: PdfLink
    category: str
    arxiv_id: Optional[ArxivId]
    summary: Optional[Summary]
    parsed_at: Optional[datetime]
    created_at: datetime
    
    def __post_init__(self):
        """Validate entity."""
        if not self.title:
            raise ValueError("Title cannot be empty")
        if not self.category:
            raise ValueError("Category cannot be empty")
    
    @classmethod
    def create(
        cls,
        title: str,
        pdf_link: str,
        category: str,
        arxiv_id: Optional[str] = None,
    ) -> "Paper":
        """Factory method to create a new paper."""
        return cls(
            id=uuid4(),
            title=title,
            pdf_link=PdfLink(pdf_link),
            category=category,
            arxiv_id=ArxivId(arxiv_id) if arxiv_id else None,
            summary=None,
            parsed_at=None,
            created_at=datetime.utcnow(),
        )
    
    def mark_as_parsed(self, summary: Summary) -> None:
        """Mark paper as parsed with summary."""
        self.summary = summary
        self.parsed_at = datetime.utcnow()
    
    def is_parsed(self) -> bool:
        """Check if paper has been parsed."""
        return self.summary is not None and self.parsed_at is not None
    
    def get_pdf_link_str(self) -> str:
        """Get PDF link as string."""
        return str(self.pdf_link)
    
    def get_arxiv_id_str(self) -> Optional[str]:
        """Get ArXiv ID as string."""
        return str(self.arxiv_id) if self.arxiv_id else None

