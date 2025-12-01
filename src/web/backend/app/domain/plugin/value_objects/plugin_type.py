"""Plugin type value object."""
from enum import Enum


class PluginType(str, Enum):
    """Plugin type enumeration."""
    
    OUTPUT = "output"
    INPUT = "input"
    PROCESSING = "processing"

