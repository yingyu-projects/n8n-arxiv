"""ArXiv ID value object."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ArxivId:
    """Immutable ArXiv ID value object."""
    
    value: str
    
    def __post_init__(self):
        """Validate ArXiv ID."""
        if not self.value:
            raise ValueError("ArXiv ID cannot be empty")
        
        # ArXiv ID format: YYMM.NNNNN or YYMM.NNNNNvN
        arxiv_pattern = re.compile(r'^\d{4}\.\d{5}(v\d+)?$')
        
        if not arxiv_pattern.match(self.value):
            raise ValueError(f"Invalid ArXiv ID format: {self.value}")
    
    def __str__(self) -> str:
        """Return string representation."""
        return self.value

