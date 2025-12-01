"""Core API interface for plugins."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from uuid import UUID

from app.domain.paper.entities.paper import Paper


class CoreAPI(ABC):
    """Core API interface that plugins can use to interact with the application.
    
    This interface provides a controlled, versioned API surface for plugins,
    ensuring strict separation between core and extension runtime.
    """
    
    # Paper operations
    @abstractmethod
    async def get_paper(self, paper_id: UUID) -> Optional[Paper]:
        """Get a paper by ID.
        
        Args:
            paper_id: Paper ID
            
        Returns:
            Paper entity or None if not found
        """
        pass
    
    @abstractmethod
    async def get_papers_by_category(self, category: str, limit: int = 10) -> List[Paper]:
        """Get papers by category.
        
        Args:
            category: Category name
            limit: Maximum number of papers to return
            
        Returns:
            List of Paper entities
        """
        pass
    
    # Configuration operations
    @abstractmethod
    async def get_config(self, key: str) -> Optional[str]:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value or None if not found
        """
        pass
    
    @abstractmethod
    async def get_project_plugin_config(
        self, 
        project_id: UUID, 
        plugin_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get project-specific plugin configuration.
        
        Args:
            project_id: Project ID
            plugin_id: Plugin ID
            
        Returns:
            Plugin configuration dictionary or None if not found
        """
        pass
    
    # Logging operations
    @abstractmethod
    def log_info(self, message: str, plugin_name: str) -> None:
        """Log an info message.
        
        Args:
            message: Log message
            plugin_name: Name of the plugin logging
        """
        pass
    
    @abstractmethod
    def log_error(self, message: str, plugin_name: str, error: Exception = None) -> None:
        """Log an error message.
        
        Args:
            message: Log message
            plugin_name: Name of the plugin logging
            error: Optional exception
        """
        pass
    
    # HTTP client operations (for external API calls)
    @abstractmethod
    async def http_get(self, url: str, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make an HTTP GET request.
        
        Args:
            url: Request URL
            headers: Optional request headers
            
        Returns:
            Response dictionary with 'status', 'headers', 'body' keys
        """
        pass
    
    @abstractmethod
    async def http_post(
        self, 
        url: str, 
        data: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Make an HTTP POST request.
        
        Args:
            url: Request URL
            data: Optional request body data
            headers: Optional request headers
            
        Returns:
            Response dictionary with 'status', 'headers', 'body' keys
        """
        pass

