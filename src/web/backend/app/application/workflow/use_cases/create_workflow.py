"""Create workflow use case."""
from typing import List, Optional

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.domain.workflow.entities.workflow import Workflow
from app.application.dto.workflow_dto import WorkflowDTO


class CreateWorkflowUseCase:
    """Use case for creating a workflow."""
    
    def __init__(self, workflow_repository: WorkflowRepository):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
    
    async def execute(
        self,
        name: str,
        categories: List[str],
        num_papers: int = 50,
        description: Optional[str] = None,
    ) -> WorkflowDTO:
        """Execute use case - create a workflow.
        
        Args:
            name: Workflow name
            categories: List of arXiv categories
            num_papers: Number of papers per category
            description: Optional workflow description
            
        Returns:
            WorkflowDTO
        """
        # Check if workflow with same name exists
        existing = await self._workflow_repository.find_by_name(name)
        if existing:
            raise ValueError(f"Workflow with name '{name}' already exists")
        
        workflow = Workflow.create(
            name=name,
            categories=categories,
            num_papers=num_papers,
            description=description,
        )
        
        workflow = await self._workflow_repository.save(workflow)
        return WorkflowDTO.from_domain(workflow)

