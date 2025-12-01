"""Delete project use case."""
from uuid import UUID

from app.domain.project.repositories.project_repository import ProjectRepository


class DeleteProjectUseCase:
    """Use case for deleting a project."""
    
    def __init__(self, project_repository: ProjectRepository):
        """Initialize use case."""
        self._project_repository = project_repository
    
    async def execute(self, project_id: UUID) -> None:
        """Execute use case - delete a project.
        
        Args:
            project_id: Project ID
            
        Raises:
            ValueError: If project not found
        """
        project = await self._project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        
        await self._project_repository.delete(project_id)

