"""Plugin ORM model."""
from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
_is_sqlite = settings.database_type == "sqlite"
_id_type = String if _is_sqlite else UUID(as_uuid=True)


class PluginORM(Base):
    """SQLAlchemy ORM model for Plugin."""
    
    __tablename__ = "plugins"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    type = Column(String, nullable=False)  # PluginType enum value
    version = Column(String, nullable=False)
    config_schema = Column(JSON, nullable=False)  # JSON schema
    enabled = Column(Boolean, nullable=False, default=True)
    plugin_metadata = Column(JSON, nullable=True)  # Plugin-specific metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

