"""Update project use case."""
from typing import Optional
from uuid import UUID

from app.domain.project.repositories.project_repository import ProjectRepository
from app.domain.project.entities.project import Project
from app.application.dto.project_dto import ProjectDTO


class UpdateProjectUseCase:
    """Use case for updating a project."""
    
    def __init__(self, project_repository: ProjectRepository):
        """Initialize use case."""
        self._project_repository = project_repository
    
    async def execute(
        self,
        project_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ProjectDTO:
        """Execute use case - update a project.
        
        Args:
            project_id: Project ID
            name: Optional new project name
            description: Optional new project description
            
        Returns:
            ProjectDTO
            
        Raises:
            ValueError: If project not found or name already exists
        """
        project = await self._project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        
        # Check if name is being changed and if new name already exists
        if name and name != project.name:
            existing = await self._project_repository.find_by_name(name)
            if existing:
                raise ValueError(f"Project with name '{name}' already exists")
            project.update_name(name)
        
        if description is not None:
            project.update_description(description)
        
        project = await self._project_repository.save(project)
        return ProjectDTO.from_domain(project)


