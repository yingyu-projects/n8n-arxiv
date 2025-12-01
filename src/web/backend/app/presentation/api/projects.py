"""Projects API routes."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID

from app.presentation.schemas.project_schema import (
    CreateProjectRequest,
    UpdateProjectRequest,
    ProjectResponse,
)
from app.application.use_cases.project.create_project import CreateProjectUseCase
from app.application.use_cases.project.get_projects import GetProjectsUseCase
from app.application.use_cases.project.get_project import GetProjectUseCase
from app.application.use_cases.project.update_project import UpdateProjectUseCase
from app.application.use_cases.project.delete_project import DeleteProjectUseCase
from app.presentation.api.dependencies import get_project_repository
from app.domain.project.repositories.project_repository import ProjectRepository


router = APIRouter()


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    """List all projects."""
    use_case = GetProjectsUseCase(project_repository)
    projects = await use_case.execute()
    return [ProjectResponse.from_dto(p) for p in projects]


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    """Get project by ID."""
    use_case = GetProjectUseCase(project_repository)
    project = await use_case.execute(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    
    return ProjectResponse.from_dto(project)


@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    request: CreateProjectRequest,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    """Create a new project."""
    use_case = CreateProjectUseCase(project_repository)
    try:
        project = await use_case.execute(
            name=request.name,
            description=request.description,
        )
        return ProjectResponse.from_dto(project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    request: UpdateProjectRequest,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    """Update a project."""
    use_case = UpdateProjectUseCase(project_repository)
    try:
        project = await use_case.execute(
            project_id=project_id,
            name=request.name,
            description=request.description,
        )
        return ProjectResponse.from_dto(project)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/projects/{project_id}", response_model=dict)
async def delete_project(
    project_id: UUID,
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    """Delete a project."""
    use_case = DeleteProjectUseCase(project_repository)
    try:
        await use_case.execute(project_id)
        return {"message": "Project deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

