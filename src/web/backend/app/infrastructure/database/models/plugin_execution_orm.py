"""Plugin execution ORM model."""
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infrastructure.database.database import Base
from app.config import settings

# Determine if using SQLite (SQLite doesn't support UUID type natively)
_is_sqlite = settings.database_type == "sqlite"
_id_type = String if _is_sqlite else UUID(as_uuid=True)
_fk_type = String if _is_sqlite else UUID(as_uuid=True)


class PluginExecutionORM(Base):
    """SQLAlchemy ORM model for PluginExecution."""
    
    __tablename__ = "plugin_executions"
    
    id = Column(_id_type, primary_key=True, default=uuid.uuid4)
    plugin_id = Column(_fk_type, ForeignKey("plugins.id"), nullable=False, index=True)
    workflow_id = Column(_fk_type, ForeignKey("workflows.id"), nullable=False, index=True)
    workflow_run_id = Column(String, nullable=False, index=True)  # Identifier for workflow execution instance
    paper_id = Column(_fk_type, ForeignKey("papers.id"), nullable=False, index=True)
    status = Column(String, nullable=False)  # PluginStatus enum value
    config = Column(JSON, nullable=False)  # Plugin configuration used for this execution
    result = Column(JSON, nullable=True)  # Execution result/error
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

