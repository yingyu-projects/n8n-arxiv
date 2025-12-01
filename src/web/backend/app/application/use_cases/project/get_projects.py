"""Get projects use case."""
from typing import List

from app.domain.project.repositories.project_repository import ProjectRepository
from app.application.dto.project_dto import ProjectDTO


class GetProjectsUseCase:
    """Use case for getting all projects."""
    
    def __init__(self, project_repository: ProjectRepository):
        """Initialize use case."""
        self._project_repository = project_repository
    
    async def execute(self) -> List[ProjectDTO]:
        """Execute use case - get all projects.
        
        Returns:
            List of ProjectDTO
        """
        projects = await self._project_repository.find_all()
        return [ProjectDTO.from_domain(project) for project in projects]

