"""Update workflow use case."""
from typing import List, Optional
from uuid import UUID

from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.application.dto.workflow_dto import WorkflowDTO


class UpdateWorkflowUseCase:
    """Use case for updating a workflow."""
    
    def __init__(self, workflow_repository: WorkflowRepository):
        """Initialize use case."""
        self._workflow_repository = workflow_repository
    
    async def execute(
        self,
        workflow_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        categories: Optional[List[str]] = None,
        num_papers: Optional[int] = None,
        enabled: Optional[bool] = None,
    ) -> WorkflowDTO:
        """Execute use case - update workflow.
        
        Args:
            workflow_id: Workflow ID
            name: Optional new name
            description: Optional new description
            categories: Optional new categories
            num_papers: Optional new num_papers
            enabled: Optional enabled status
            
        Returns:
            WorkflowDTO
        """
        workflow = await self._workflow_repository.find_by_id(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")
        
        if name is not None:
            # Check if name is already taken by another workflow
            existing = await self._workflow_repository.find_by_name(name)
            if existing and existing.id != workflow_id:
                raise ValueError(f"Workflow with name '{name}' already exists")
            # Note: We can't directly change name in the entity, need to recreate
            # For now, we'll skip name updates or handle them separately
        
        if description is not None:
            workflow.update_description(description)
        
        if categories is not None:
            workflow.update_categories(categories)
        
        if num_papers is not None:
            workflow.update_num_papers(num_papers)
        
        if enabled is not None:
            if enabled:
                workflow.enable()
            else:
                workflow.disable()
        
        workflow = await self._workflow_repository.save(workflow)
        return WorkflowDTO.from_domain(workflow)

