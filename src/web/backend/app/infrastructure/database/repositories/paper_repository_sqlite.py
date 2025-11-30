"""Paper repository implementation for SQLite."""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.paper.entities.paper import Paper
from app.infrastructure.database.models.paper_orm import PaperORM
from app.infrastructure.mappers.paper_mapper import PaperMapper


class PaperRepositorySQLite(PaperRepository):
    """SQLite-specific implementation of PaperRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, paper: Paper) -> Paper:
        """Save a paper."""
        # Convert UUID to string for SQLite
        paper_id = str(paper.id)
        existing = self._session.query(PaperORM).filter(
            PaperORM.id == paper_id
        ).first()
        
        if existing:
            PaperMapper.update_orm_from_domain(existing, paper)
            self._session.commit()
            self._session.refresh(existing)
            return PaperMapper.to_domain(existing)
        else:
            # Convert UUID to string for SQLite
            orm = PaperMapper.to_orm(paper, convert_uuid_to_string=True)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return PaperMapper.to_domain(orm)
    
    async def find_by_id(self, paper_id: UUID) -> Optional[Paper]:
        """Find paper by ID."""
        # Convert UUID to string for SQLite
        query_id = str(paper_id)
        orm = self._session.query(PaperORM).filter(
            PaperORM.id == query_id
        ).first()
        
        return PaperMapper.to_domain(orm) if orm else None
    
    async def find_by_pdf_link(self, pdf_link: str) -> Optional[Paper]:
        """Find paper by PDF link."""
        orm = self._session.query(PaperORM).filter(
            PaperORM.pdf_link == pdf_link
        ).first()
        
        return PaperMapper.to_domain(orm) if orm else None
    
    async def find_all(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Paper]:
        """Find all papers with optional filtering."""
        query = self._session.query(PaperORM)
        
        if category:
            query = query.filter(PaperORM.category == category)
        
        query = query.order_by(PaperORM.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        orms = query.all()
        return [PaperMapper.to_domain(orm) for orm in orms]
    
    async def exists_by_pdf_link(self, pdf_link: str) -> bool:
        """Check if paper exists by PDF link."""
        count = self._session.query(PaperORM).filter(
            PaperORM.pdf_link == pdf_link
        ).count()
        
        return count > 0

