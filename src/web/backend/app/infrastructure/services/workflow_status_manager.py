"""Workflow status manager for tracking parsing progress."""
from typing import Dict, Optional
from datetime import datetime
import asyncio
from enum import Enum


class WorkflowStatus(str, Enum):
    """Workflow status enum."""
    IDLE = "idle"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    COMPLETED = "completed"
    ERROR = "error"


class WorkflowStatusManager:
    """Manages workflow execution status and progress."""
    
    def __init__(self):
        """Initialize status manager."""
        self._status: WorkflowStatus = WorkflowStatus.IDLE
        self._total_papers: int = 0
        self._processed: int = 0
        self._skipped: int = 0
        self._errors: list[str] = []
        self._papers: list[Dict[str, any]] = []
        self._start_time: Optional[datetime] = None
        self._stop_requested: bool = False
        self._lock = asyncio.Lock()
    
    async def start_workflow(self, total_papers: int) -> None:
        """Start a new workflow."""
        async with self._lock:
            self._status = WorkflowStatus.RUNNING
            self._total_papers = total_papers
            self._processed = 0
            self._skipped = 0
            self._errors = []
            self._papers = []
            self._start_time = datetime.utcnow()
            self._stop_requested = False
    
    async def update_progress(
        self,
        processed: int = 0,
        skipped: int = 0,
        errors: Optional[list[str]] = None,
        papers: Optional[list[Dict[str, any]]] = None,
    ) -> None:
        """Update workflow progress."""
        async with self._lock:
            self._processed += processed
            self._skipped += skipped
            if errors:
                self._errors.extend(errors)
            if papers:
                self._papers.extend(papers)
    
    async def complete_workflow(self) -> None:
        """Mark workflow as completed."""
        async with self._lock:
            self._status = WorkflowStatus.COMPLETED
    
    async def stop_workflow(self) -> None:
        """Request workflow to stop."""
        async with self._lock:
            if self._status == WorkflowStatus.RUNNING:
                self._status = WorkflowStatus.STOPPING
                self._stop_requested = True
    
    async def mark_stopped(self) -> None:
        """Mark workflow as stopped."""
        async with self._lock:
            self._status = WorkflowStatus.STOPPED
    
    async def mark_error(self, error: str) -> None:
        """Mark workflow as error."""
        async with self._lock:
            self._status = WorkflowStatus.ERROR
            self._errors.append(error)
    
    async def should_stop(self) -> bool:
        """Check if workflow should stop."""
        async with self._lock:
            return self._stop_requested
    
    async def get_status(self) -> Dict[str, any]:
        """Get current workflow status."""
        async with self._lock:
            elapsed_time = None
            if self._start_time:
                elapsed_time = (datetime.utcnow() - self._start_time).total_seconds()
            
            return {
                "status": self._status.value,
                "total_papers": self._total_papers,
                "processed": self._processed,
                "skipped": self._skipped,
                "errors": self._errors.copy(),
                "papers": self._papers.copy(),
                "elapsed_time": elapsed_time,
            }
    
    async def reset(self) -> None:
        """Reset status manager."""
        async with self._lock:
            self._status = WorkflowStatus.IDLE
            self._total_papers = 0
            self._processed = 0
            self._skipped = 0
            self._errors = []
            self._papers = []
            self._start_time = None
            self._stop_requested = False


# Global instance
workflow_status_manager = WorkflowStatusManager()

