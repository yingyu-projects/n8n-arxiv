"""Workflow plugin configuration ORM model."""
from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
_is_sqlite = settings.database_type == "sqlite"
_id_type = String if _is_sqlite else UUID(as_uuid=True)
_fk_type = String if _is_sqlite else UUID(as_uuid=True)


class WorkflowPluginConfigORM(Base):
    """SQLAlchemy ORM model for WorkflowPluginConfig."""
    
    __tablename__ = "workflow_plugin_configs"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    workflow_id = Column(_fk_type, ForeignKey("workflows.id"), nullable=False, index=True)
    plugin_id = Column(_fk_type, ForeignKey("plugins.id"), nullable=False, index=True)
    enabled = Column(Boolean, nullable=False, default=True)
    config = Column(JSON, nullable=False)  # Plugin configuration values
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint on (workflow_id, plugin_id)
    __table_args__ = (
        UniqueConstraint('workflow_id', 'plugin_id', name='uq_workflow_plugin'),
    )

