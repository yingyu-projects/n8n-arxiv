"""Workflow ORM model."""
from sqlalchemy import Column, String, DateTime, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
_is_sqlite = settings.database_type == "sqlite"
_id_type = String if _is_sqlite else UUID(as_uuid=True)


class WorkflowORM(Base):
    """SQLAlchemy ORM model for Workflow."""
    
    __tablename__ = "workflows"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    categories = Column(JSON, nullable=False)  # Array of category strings
    num_papers = Column(Integer, nullable=False, default=50)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

