"""Config API routes."""
from fastapi import APIRouter, Depends, Query, HTTPException

from app.presentation.schemas.config_schema import (
    ConfigResponse,
    UpdateConfigRequest,
    GetConfigResponse,
)
from app.application.use_cases.config.get_config import GetConfigUseCase
from app.application.use_cases.config.update_config import UpdateConfigUseCase
from app.presentation.api.dependencies import get_config_repository
from app.domain.config.repositories.config_repository import ConfigRepository


router = APIRouter()


@router.get("/config", response_model=GetConfigResponse)
async def get_config(
    key: str = Query(..., description="Config key"),
    config_repository: ConfigRepository = Depends(get_config_repository),
):
    """Get config by key."""
    use_case = GetConfigUseCase(config_repository)
    config = await use_case.execute(key)
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Config with key '{key}' not found")
    
    return GetConfigResponse(
        key=config.key,
        value=config.value,
    )


@router.post("/config", response_model=ConfigResponse)
async def update_config(
    request: UpdateConfigRequest,
    config_repository: ConfigRepository = Depends(get_config_repository),
):
    """Update config (creates if not exists)."""
    use_case = UpdateConfigUseCase(config_repository)
    config = await use_case.execute(request.key, request.value)
    
    return ConfigResponse(
        id=config.id,
        key=config.key,
        value=config.value,
    )

