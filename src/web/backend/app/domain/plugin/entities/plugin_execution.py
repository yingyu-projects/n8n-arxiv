"""Plugin execution domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID, uuid4

from app.domain.plugin.value_objects.plugin_status import PluginStatus


@dataclass
class PluginExecution:
    """Plugin execution tracking entity."""
    
    id: UUID
    plugin_id: UUID
    workflow_id: UUID
    workflow_run_id: str
    paper_id: UUID
    status: PluginStatus
    config: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime]
    
    def __post_init__(self):
        """Validate entity."""
        if not self.workflow_run_id:
            raise ValueError("Workflow run ID cannot be empty")
        if self.config is None:
            self.config = {}
    
    @classmethod
    def create(
        cls,
        plugin_id: UUID,
        workflow_id: UUID,
        workflow_run_id: str,
        paper_id: UUID,
        config: Dict[str, Any],
    ) -> "PluginExecution":
        """Factory method to create a new plugin execution."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            plugin_id=plugin_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            paper_id=paper_id,
            status=PluginStatus.PENDING,
            config=config or {},
            result=None,
            started_at=now,
            completed_at=None,
        )
    
    def mark_running(self) -> None:
        """Mark execution as running."""
        self.status = PluginStatus.RUNNING
    
    def mark_success(self, result: Optional[Dict[str, Any]] = None) -> None:
        """Mark execution as successful."""
        self.status = PluginStatus.SUCCESS
        self.result = result
        self.completed_at = datetime.utcnow()
    
    def mark_failed(self, error: str) -> None:
        """Mark execution as failed."""
        self.status = PluginStatus.FAILED
        self.result = {"error": error}
        self.completed_at = datetime.utcnow()

