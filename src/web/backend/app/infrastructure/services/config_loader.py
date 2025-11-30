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
            # __file__ is at app/infrastructure/services/config_loader.py
            # Go up 3 levels to get to backend directory
            backend_dir = Path(__file__).parent.parent.parent.parent
            config_path = backend_dir / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file.
        
        Raises:
            FileNotFoundError: If config file does not exist
            Exception: If config file cannot be read or parsed
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}. "
                "Please create config/config.yaml with required database and LLM settings."
            )
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
                
            # Validate required configuration sections
            if not config.get("database"):
                raise ValueError(
                    "Missing 'database' section in config.yaml. "
                    "Please specify 'database.type' and 'database.url'."
                )
            
            return config
        except FileNotFoundError:
            raise
        except ValueError:
            raise
        except Exception as e:
            raise Exception(f"Failed to load config from {self.config_path}: {str(e)}")

