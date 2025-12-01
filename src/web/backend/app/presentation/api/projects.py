"""Projects API routes."""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import UUID

from app.presentation.schemas.project_schema import (
    CreateProjectRequest,
    UpdateProjectRequest,
    ProjectResponse,
    ProjectPluginConfigResponse,
    UpdateProjectPluginConfigRequest,
)
from app.application.use_cases.project.create_project import CreateProjectUseCase
from app.application.use_cases.project.get_projects import GetProjectsUseCase
from app.application.use_cases.project.get_project import GetProjectUseCase
from app.application.use_cases.project.update_project import UpdateProjectUseCase
from app.application.use_cases.project.delete_project import DeleteProjectUseCase
from app.application.use_cases.project.get_project_plugin_config import GetProjectPluginConfigUseCase
from app.application.use_cases.project.get_project_plugin_configs import GetProjectPluginConfigsUseCase
from app.application.use_cases.project.update_project_plugin_config import UpdateProjectPluginConfigUseCase
from app.presentation.api.dependencies import (
    get_project_repository,
    get_project_plugin_config_repository,
)
from app.domain.project.repositories.project_repository import ProjectRepository
from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository


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


@router.get("/projects/{project_id}/plugin-configs", response_model=List[ProjectPluginConfigResponse])
async def get_project_plugin_configs(
    project_id: UUID,
    project_plugin_config_repository: ProjectPluginConfigRepository = Depends(get_project_plugin_config_repository),
):
    """Get all plugin configs for a project."""
    use_case = GetProjectPluginConfigsUseCase(project_plugin_config_repository)
    configs = await use_case.execute(project_id)
    return [ProjectPluginConfigResponse.from_dto(c) for c in configs]


@router.get("/projects/{project_id}/plugin-configs/{plugin_id}", response_model=ProjectPluginConfigResponse)
async def get_project_plugin_config(
    project_id: UUID,
    plugin_id: UUID,
    project_plugin_config_repository: ProjectPluginConfigRepository = Depends(get_project_plugin_config_repository),
):
    """Get plugin config for a project."""
    use_case = GetProjectPluginConfigUseCase(project_plugin_config_repository)
    config = await use_case.execute(project_id, plugin_id)
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Plugin config for project {project_id} and plugin {plugin_id} not found"
        )
    
    return ProjectPluginConfigResponse.from_dto(config)


@router.put("/projects/{project_id}/plugin-configs/{plugin_id}", response_model=ProjectPluginConfigResponse)
async def update_project_plugin_config(
    project_id: UUID,
    plugin_id: UUID,
    request: UpdateProjectPluginConfigRequest,
    project_plugin_config_repository: ProjectPluginConfigRepository = Depends(get_project_plugin_config_repository),
):
    """Update or create plugin config for a project."""
    use_case = UpdateProjectPluginConfigUseCase(project_plugin_config_repository)
    config = await use_case.execute(project_id, plugin_id, request.config)
    return ProjectPluginConfigResponse.from_dto(config)

