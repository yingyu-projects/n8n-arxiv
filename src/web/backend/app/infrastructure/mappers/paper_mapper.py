"""Mapper between Paper ORM and Domain entity."""
from datetime import datetime
from typing import Optional
import uuid

from app.domain.paper.entities.paper import Paper
from app.domain.paper.value_objects.pdf_link import PdfLink
from app.domain.paper.value_objects.arxiv_id import ArxivId
from app.domain.paper.value_objects.summary import Summary
from app.infrastructure.database.models.paper_orm import PaperORM
from app.config import settings


class PaperMapper:
    """Mapper for converting between Paper ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: PaperORM) -> Paper:
        """Convert ORM model to domain entity."""
        return Paper(
            id=PaperMapper._ensure_uuid(orm.id),
            title=orm.title,
            pdf_link=PdfLink(orm.pdf_link),
            category=orm.category,
            arxiv_id=ArxivId(orm.arxiv_id) if orm.arxiv_id else None,
            summary=Summary.from_dict(orm.summary) if orm.summary else None,
            parsed_at=orm.parsed_at,
            created_at=orm.created_at,
        )
    
    @staticmethod
    def to_orm(domain: Paper, convert_uuid_to_string: bool = False) -> PaperORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        paper_id = str(domain.id) if convert_uuid_to_string else domain.id
        
        return PaperORM(
            id=paper_id,
            title=domain.title,
            pdf_link=domain.get_pdf_link_str(),
            arxiv_id=domain.get_arxiv_id_str(),
            category=domain.category,
            summary=domain.summary.to_dict() if domain.summary else None,
            parsed_at=domain.parsed_at,
            created_at=domain.created_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: PaperORM, domain: Paper) -> None:
        """Update ORM model from domain entity."""
        orm.title = domain.title
        orm.pdf_link = domain.get_pdf_link_str()
        orm.arxiv_id = domain.get_arxiv_id_str()
        orm.category = domain.category
        orm.summary = domain.summary.to_dict() if domain.summary else None
        orm.parsed_at = domain.parsed_at
        orm.created_at = domain.created_at

