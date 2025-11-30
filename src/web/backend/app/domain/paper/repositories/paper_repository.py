"""Paper repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.domain.paper.entities.paper import Paper


class PaperRepository(ABC):
    """Abstract repository interface for Paper entity."""
    
    @abstractmethod
    async def save(self, paper: Paper) -> Paper:
        """Save a paper."""
        pass
    
    @abstractmethod
    async def find_by_id(self, paper_id: UUID) -> Optional[Paper]:
        """Find paper by ID."""
        pass
    
    @abstractmethod
    async def find_by_pdf_link(self, pdf_link: str) -> Optional[Paper]:
        """Find paper by PDF link."""
        pass
    
    @abstractmethod
    async def find_all(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Paper]:
        """Find all papers with optional filtering."""
        pass
    
    @abstractmethod
    async def exists_by_pdf_link(self, pdf_link: str) -> bool:
        """Check if paper exists by PDF link."""
        pass

