"""Core API implementation."""
import logging
from typing import Dict, Any, List, Optional
from uuid import UUID

import httpx
from app.domain.paper.entities.paper import Paper
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository
from app.application.plugin.core_api import CoreAPI

logger = logging.getLogger(__name__)


class CoreAPIImpl(CoreAPI):
    """Concrete implementation of CoreAPI."""
    
    def __init__(
        self,
        paper_repository: PaperRepository,
        config_repository: ConfigRepository,
        project_plugin_config_repository: ProjectPluginConfigRepository,
    ):
        """Initialize Core API implementation.
        
        Args:
            paper_repository: Paper repository
            config_repository: Config repository
            project_plugin_config_repository: Project plugin config repository
        """
        self._paper_repository = paper_repository
        self._config_repository = config_repository
        self._project_plugin_config_repository = project_plugin_config_repository
    
    async def get_paper(self, paper_id: UUID) -> Optional[Paper]:
        """Get a paper by ID."""
        return await self._paper_repository.find_by_id(paper_id)
    
    async def get_papers_by_category(self, category: str, limit: int = 10) -> List[Paper]:
        """Get papers by category."""
        papers = await self._paper_repository.find_all(
            category=category,
            limit=limit,
            offset=0
        )
        return papers
    
    async def get_config(self, key: str) -> Optional[str]:
        """Get a configuration value."""
        config = await self._config_repository.find_by_key(key)
        return config.value if config else None
    
    async def get_project_plugin_config(
        self, 
        project_id: UUID, 
        plugin_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get project-specific plugin configuration."""
        config = await self._project_plugin_config_repository.find_by_project_and_plugin(
            project_id, plugin_id
        )
        return config.config if config else None
    
    def log_info(self, message: str, plugin_name: str) -> None:
        """Log an info message."""
        logger.info(f"[Plugin: {plugin_name}] {message}")
    
    def log_error(self, message: str, plugin_name: str, error: Exception = None) -> None:
        """Log an error message."""
        if error:
            logger.error(f"[Plugin: {plugin_name}] {message}: {error}", exc_info=error)
        else:
            logger.error(f"[Plugin: {plugin_name}] {message}")
    
    async def http_get(self, url: str, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make an HTTP GET request."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers or {}, timeout=30.0)
                return {
                    'status': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            except httpx.HTTPError as e:
                raise Exception(f"HTTP GET request failed: {str(e)}")
    
    async def http_post(
        self, 
        url: str, 
        data: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Make an HTTP POST request."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data, headers=headers or {}, timeout=30.0)
                return {
                    'status': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            except httpx.HTTPError as e:
                raise Exception(f"HTTP POST request failed: {str(e)}")

