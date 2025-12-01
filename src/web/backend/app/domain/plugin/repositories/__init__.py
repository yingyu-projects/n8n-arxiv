"""Plugin repositories."""
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.repositories.plugin_execution_repository import PluginExecutionRepository

__all__ = ["PluginRepository", "PluginExecutionRepository"]

