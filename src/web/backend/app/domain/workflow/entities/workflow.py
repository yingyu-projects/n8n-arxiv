"""Workflow domain entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class Workflow:
    """Workflow domain entity with business logic."""
    
    id: UUID
    name: str
    description: Optional[str]
    categories: List[str]
    num_papers: int
    enabled: bool
    project_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate entity."""
        if not self.name:
            raise ValueError("Workflow name cannot be empty")
        if not self.categories:
            raise ValueError("Workflow must have at least one category")
        if self.num_papers < 1:
            raise ValueError("Number of papers must be at least 1")
    
    @classmethod
    def create(
        cls,
        name: str,
        categories: List[str],
        project_id: Optional[UUID],
        num_papers: int = 50,
        description: Optional[str] = None,
    ) -> "Workflow":
        """Factory method to create a new workflow."""
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            categories=categories,
            num_papers=num_papers,
            enabled=True,
            project_id=project_id,
            created_at=now,
            updated_at=now,
        )
    
    def enable(self) -> None:
        """Enable workflow."""
        self.enabled = True
        self.updated_at = datetime.utcnow()
    
    def disable(self) -> None:
        """Disable workflow."""
        self.enabled = False
        self.updated_at = datetime.utcnow()
    
    def update_categories(self, categories: List[str]) -> None:
        """Update workflow categories."""
        if not categories:
            raise ValueError("Workflow must have at least one category")
        self.categories = categories
        self.updated_at = datetime.utcnow()
    
    def update_num_papers(self, num_papers: int) -> None:
        """Update number of papers."""
        if num_papers < 1:
            raise ValueError("Number of papers must be at least 1")
        self.num_papers = num_papers
        self.updated_at = datetime.utcnow()
    
    def update_description(self, description: Optional[str]) -> None:
        """Update workflow description."""
        self.description = description
        self.updated_at = datetime.utcnow()

