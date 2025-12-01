"""Plugin execution status value object."""
from enum import Enum


class PluginStatus(str, Enum):
    """Plugin execution status enumeration."""
    
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

