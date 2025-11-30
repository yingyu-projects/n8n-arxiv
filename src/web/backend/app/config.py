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
        
        # Database configuration - REQUIRED, no defaults
        database_config = self._config.get("database", {})
        
        # Database type: "sqlite" or "postgresql" - REQUIRED
        db_type = database_config.get("type")
        if not db_type:
            raise ValueError(
                "Database type is required in config.yaml. "
                "Please specify 'database.type' as 'sqlite' or 'postgresql'."
            )
        
        if db_type not in ["sqlite", "postgresql"]:
            raise ValueError(
                f"Invalid database type: {db_type}. "
                "Must be 'sqlite' or 'postgresql'."
            )
        
        self.database_type: str = db_type
        
        # Database URL - REQUIRED (can be overridden by DATABASE_URL env var)
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            db_url = database_config.get("url")
            if not db_url:
                raise ValueError(
                    "Database URL is required. "
                    "Please specify 'database.url' in config.yaml or set DATABASE_URL environment variable."
                )
        
        self.database_url: str = db_url
        
        # API
        self.api_title: str = "arXiv Parser API"
        self.api_version: str = "1.0.0"
        self.api_prefix: str = "/api"
        
        # CORS
        self.cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()

