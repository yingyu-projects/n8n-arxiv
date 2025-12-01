"""Create project use case."""
from typing import Optional

from app.domain.project.repositories.project_repository import ProjectRepository
from app.domain.project.entities.project import Project
from app.application.dto.project_dto import ProjectDTO


class CreateProjectUseCase:
    """Use case for creating a project."""
    
    def __init__(self, project_repository: ProjectRepository):
        """Initialize use case."""
        self._project_repository = project_repository
    
    async def execute(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> ProjectDTO:
        """Execute use case - create a project.
        
        Args:
            name: Project name
            description: Optional project description
            
        Returns:
            ProjectDTO
        """
        # Check if project with same name exists
        existing = await self._project_repository.find_by_name(name)
        if existing:
            raise ValueError(f"Project with name '{name}' already exists")
        
        project = Project.create(
            name=name,
            description=description,
        )
        
        project = await self._project_repository.save(project)
        return ProjectDTO.from_domain(project)

