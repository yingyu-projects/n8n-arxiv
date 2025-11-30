"""Config ORM model."""
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
# Use database_type from settings for explicit configuration
_is_sqlite = settings.database_type == "sqlite"
_id_type = String if _is_sqlite else UUID(as_uuid=True)


class ConfigORM(Base):
    """SQLAlchemy ORM model for Config."""
    
    __tablename__ = "configs"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)

