"""Application configuration."""
import os
from typing import List
from app.infrastructure.services.config_loader import ConfigLoader


class Settings:
    """Application settings loaded from config.yaml or environment variables.
    
    Environment variables take precedence over config.yaml values.
    """
    
    def __init__(self):
        """Initialize settings from config file."""
        config_loader = ConfigLoader()
        self._config = config_loader.load_config()
        
        # Database - check environment variable first, then config.yaml, then default
        # Default to SQLite for local development
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            self._config.get("database", {}).get(
                "url",
                "sqlite:///./arxiv_db.sqlite"
            )
        )
        
        # API
        self.api_title: str = "arXiv Parser API"
        self.api_version: str = "1.0.0"
        self.api_prefix: str = "/api"
        
        # CORS
        self.cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()

