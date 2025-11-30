"""Dependency injection for API routes."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.category.repositories.category_repository import CategoryRepository
from app.infrastructure.database.repositories.paper_repository_impl import PaperRepositoryImpl
from app.infrastructure.database.repositories.category_repository_impl import CategoryRepositoryImpl
from app.infrastructure.external.arxiv_client import ArxivClient
from app.infrastructure.external.pdf_client import PdfClient
from app.infrastructure.services.text_cleaner import TextCleaner
from app.infrastructure.services.config_loader import ConfigLoader


def get_paper_repository(db: Session = Depends(get_db)) -> PaperRepository:
    """Get paper repository."""
    return PaperRepositoryImpl(db)


def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    """Get category repository."""
    return CategoryRepositoryImpl(db)


def get_arxiv_client() -> ArxivClient:
    """Get arXiv client."""
    return ArxivClient()


def get_pdf_client() -> PdfClient:
    """Get PDF client."""
    return PdfClient()


def get_text_cleaner() -> TextCleaner:
    """Get text cleaner."""
    return TextCleaner()


def get_config_loader() -> ConfigLoader:
    """Get config loader."""
    return ConfigLoader()

