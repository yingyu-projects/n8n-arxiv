"""PDF Link value object."""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class PdfLink:
    """Immutable PDF link value object."""
    
    value: str
    
    def __post_init__(self):
        """Validate PDF link."""
        if not self.value:
            raise ValueError("PDF link cannot be empty")
        
        # Validate it's a valid URL
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(self.value):
            raise ValueError(f"Invalid PDF link URL: {self.value}")
    
    def __str__(self) -> str:
        """Return string representation."""
        return self.value

