"""Config API schemas."""
from pydantic import BaseModel
from uuid import UUID


class ConfigResponse(BaseModel):
    """Config response schema."""
    
    id: UUID
    key: str
    value: str
    
    class Config:
        from_attributes = True


class UpdateConfigRequest(BaseModel):
    """Update config request schema."""
    
    key: str
    value: str


class GetConfigResponse(BaseModel):
    """Get config response schema."""
    
    key: str
    value: str

