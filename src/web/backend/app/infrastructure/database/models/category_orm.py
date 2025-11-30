"""Category ORM model."""
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
_is_sqlite = settings.database_url.startswith("sqlite")
_id_type = String if _is_sqlite else UUID(as_uuid=True)


class CategoryORM(Base):
    """SQLAlchemy ORM model for Category."""
    
    __tablename__ = "categories"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    enabled = Column(Boolean, nullable=False, default=True)
    num_papers = Column(Integer, nullable=False, default=0)

