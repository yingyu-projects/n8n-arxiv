"""Configuration loader service."""
import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigLoader:
    """Service for loading configuration from YAML file."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config loader."""
        if config_path is None:
            # Default to config/config.yaml relative to backend directory
            backend_dir = Path(__file__).parent.parent.parent
            config_path = backend_dir / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            # Return default config
            return {
                "database": {
                    "url": "sqlite:///./arxiv_db.sqlite"
                },
                "llm": {
                    "provider": "local",
                    "local": {
                        "base_url": "http://127.0.0.1:1234",
                        "model": "qwen/qwen3-vl-8b",
                        "endpoint": "/v1/responses"
                    },
                    "openai": {
                        "api_key": "",
                        "model": "gpt-4"
                    }
                }
            }
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise Exception(f"Failed to load config: {str(e)}")

