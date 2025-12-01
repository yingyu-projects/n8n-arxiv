"""Repository implementations."""
from app.config import settings
from sqlalchemy.orm import Session

# Import all repository implementations
from app.infrastructure.database.repositories.paper_repository_sqlite import PaperRepositorySQLite
from app.infrastructure.database.repositories.paper_repository_postgres import PaperRepositoryPostgres
from app.infrastructure.database.repositories.category_repository_sqlite import CategoryRepositorySQLite
from app.infrastructure.database.repositories.category_repository_postgres import CategoryRepositoryPostgres
from app.infrastructure.database.repositories.config_repository_sqlite import ConfigRepositorySQLite
from app.infrastructure.database.repositories.config_repository_postgres import ConfigRepositoryPostgres
from app.infrastructure.database.repositories.workflow_repository_sqlite import WorkflowRepositorySQLite
from app.infrastructure.database.repositories.workflow_repository_postgres import WorkflowRepositoryPostgres
from app.infrastructure.database.repositories.workflow_plugin_config_repository_sqlite import WorkflowPluginConfigRepositorySQLite
from app.infrastructure.database.repositories.workflow_plugin_config_repository_postgres import WorkflowPluginConfigRepositoryPostgres
from app.infrastructure.database.repositories.plugin_repository_sqlite import PluginRepositorySQLite
from app.infrastructure.database.repositories.plugin_repository_postgres import PluginRepositoryPostgres
from app.infrastructure.database.repositories.plugin_execution_repository_sqlite import PluginExecutionRepositorySQLite
from app.infrastructure.database.repositories.plugin_execution_repository_postgres import PluginExecutionRepositoryPostgres

# Import repository interfaces
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.category.repositories.category_repository import CategoryRepository
from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.repositories.plugin_execution_repository import PluginExecutionRepository


def create_paper_repository(session: Session) -> PaperRepository:
    """Factory function to create the appropriate paper repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return PaperRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return PaperRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")


def create_category_repository(session: Session) -> CategoryRepository:
    """Factory function to create the appropriate category repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return CategoryRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return CategoryRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")


def create_config_repository(session: Session) -> ConfigRepository:
    """Factory function to create the appropriate config repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return ConfigRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return ConfigRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")


def create_workflow_repository(session: Session) -> WorkflowRepository:
    """Factory function to create the appropriate workflow repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return WorkflowRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return WorkflowRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")


def create_workflow_plugin_config_repository(session: Session) -> WorkflowPluginConfigRepository:
    """Factory function to create the appropriate workflow plugin config repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return WorkflowPluginConfigRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return WorkflowPluginConfigRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")


def create_plugin_repository(session: Session) -> PluginRepository:
    """Factory function to create the appropriate plugin repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return PluginRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return PluginRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")


def create_plugin_execution_repository(session: Session) -> PluginExecutionRepository:
    """Factory function to create the appropriate plugin execution repository implementation.
    
    Uses the database type from configuration to select the correct implementation.
    """
    if settings.database_type == "sqlite":
        return PluginExecutionRepositorySQLite(session)
    elif settings.database_type == "postgresql":
        return PluginExecutionRepositoryPostgres(session)
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}. Must be 'sqlite' or 'postgresql'.")
