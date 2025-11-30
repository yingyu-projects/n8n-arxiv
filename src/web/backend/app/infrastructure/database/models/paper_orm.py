"""Paper ORM model."""
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
_is_sqlite = settings.database_url.startswith("sqlite")
_id_type = String if _is_sqlite else UUID(as_uuid=True)


class PaperORM(Base):
    """SQLAlchemy ORM model for Paper."""
    
    __tablename__ = "papers"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    pdf_link = Column(String, unique=True, nullable=False, index=True)
    arxiv_id = Column(String, nullable=True)
    category = Column(String, nullable=False)
    summary = Column(JSON, nullable=True)
    parsed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

