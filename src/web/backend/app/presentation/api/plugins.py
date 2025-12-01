"""Plugins API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.presentation.schemas.plugin_schema import (
    PluginResponse,
    PluginConfigSchemaResponse,
)
from app.application.plugin.use_cases.get_plugins import GetPluginsUseCase
from app.application.plugin.use_cases.get_plugin_config_schema import GetPluginConfigSchemaUseCase
from app.application.plugin.plugin_registry import PluginRegistry
from app.presentation.api.dependencies import (
    get_plugin_repository,
    get_plugin_registry,
)
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.value_objects.plugin_type import PluginType


router = APIRouter()


@router.get("/plugins", response_model=List[PluginResponse])
async def list_plugins(
    plugin_type: Optional[str] = Query(None, description="Filter by plugin type"),
    enabled_only: bool = Query(False, description="Only return enabled plugins"),
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
):
    """List all registered plugins."""
    use_case = GetPluginsUseCase(plugin_repository)
    
    plugin_type_enum = None
    if plugin_type:
        try:
            plugin_type_enum = PluginType(plugin_type.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid plugin type: {plugin_type}. Must be one of: {[t.value for t in PluginType]}"
            )
    
    plugins = await use_case.execute(
        plugin_type=plugin_type_enum,
        enabled_only=enabled_only,
    )
    
    return [PluginResponse.from_dto(p) for p in plugins]


@router.get("/plugins/{plugin_id}", response_model=PluginResponse)
async def get_plugin(
    plugin_id: UUID,
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
):
    """Get plugin by ID."""
    plugin = await plugin_repository.find_by_id(plugin_id)
    
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin with ID {plugin_id} not found")
    
    from app.application.dto.plugin_dto import PluginDTO
    plugin_dto = PluginDTO.from_domain(plugin)
    return PluginResponse.from_dto(plugin_dto)


@router.get("/plugins/{plugin_id}/config-schema", response_model=PluginConfigSchemaResponse)
async def get_plugin_config_schema(
    plugin_id: UUID,
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
):
    """Get plugin configuration schema."""
    use_case = GetPluginConfigSchemaUseCase(plugin_repository)
    schema = await use_case.execute(plugin_id)
    
    if not schema:
        raise HTTPException(status_code=404, detail=f"Plugin with ID {plugin_id} not found")
    
    return PluginConfigSchemaResponse(schema=schema)


@router.post("/plugins/discover", response_model=Dict[str, Any])
async def discover_plugins(
    plugin_registry: PluginRegistry = Depends(get_plugin_registry),
):
    """Discover and register plugins from filesystem."""
    registered = await plugin_registry.discover_and_register_plugins()
    return {
        "message": f"Discovered and registered {len(registered)} plugins",
        "count": len(registered),
    }

