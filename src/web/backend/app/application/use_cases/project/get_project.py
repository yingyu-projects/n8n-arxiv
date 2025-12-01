"""Get project use case."""
from typing import Optional
from uuid import UUID

from app.domain.project.repositories.project_repository import ProjectRepository
from app.application.dto.project_dto import ProjectDTO


class GetProjectUseCase:
    """Use case for getting a project by ID."""
    
    def __init__(self, project_repository: ProjectRepository):
        """Initialize use case."""
        self._project_repository = project_repository
    
    async def execute(self, project_id: UUID) -> Optional[ProjectDTO]:
        """Execute use case - get project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            ProjectDTO or None if not found
        """
        project = await self._project_repository.find_by_id(project_id)
        return ProjectDTO.from_domain(project) if project else None


