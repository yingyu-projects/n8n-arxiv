"""Dependency injection for API routes."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.category.repositories.category_repository import CategoryRepository
from app.domain.config.repositories.config_repository import ConfigRepository
from app.domain.workflow.repositories.workflow_repository import WorkflowRepository
from app.domain.workflow.repositories.workflow_plugin_config_repository import WorkflowPluginConfigRepository
from app.domain.plugin.repositories.plugin_repository import PluginRepository
from app.domain.plugin.repositories.plugin_execution_repository import PluginExecutionRepository
from app.domain.project.repositories.project_repository import ProjectRepository
from app.domain.project.repositories.project_plugin_config_repository import ProjectPluginConfigRepository
from app.application.plugin.core_api import CoreAPI
from app.application.plugin.core_api_impl import CoreAPIImpl
from app.infrastructure.database.repositories import (
    create_paper_repository,
    create_category_repository,
    create_config_repository,
    create_workflow_repository,
    create_workflow_plugin_config_repository,
    create_plugin_repository,
    create_plugin_execution_repository,
    create_project_repository,
    create_project_plugin_config_repository,
)
from app.infrastructure.external.arxiv_client import ArxivClient
from app.infrastructure.external.pdf_client import PdfClient
from app.infrastructure.services.text_cleaner import TextCleaner
from app.infrastructure.services.config_loader import ConfigLoader
from app.application.plugin.plugin_registry import PluginRegistry
from app.application.plugin.plugin_executor import PluginExecutor
from app.infrastructure.plugin.plugin_loader import PluginLoader


def get_paper_repository(db: Session = Depends(get_db)) -> PaperRepository:
    """Get paper repository (factory selects SQLite or PostgreSQL implementation)."""
    return create_paper_repository(db)


def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    """Get category repository (factory selects SQLite or PostgreSQL implementation)."""
    return create_category_repository(db)


def get_config_repository(db: Session = Depends(get_db)) -> ConfigRepository:
    """Get config repository (factory selects SQLite or PostgreSQL implementation)."""
    return create_config_repository(db)


def get_arxiv_client() -> ArxivClient:
    """Get arXiv client."""
    return ArxivClient()


def get_pdf_client() -> PdfClient:
    """Get PDF client."""
    return PdfClient()


def get_text_cleaner() -> TextCleaner:
    """Get text cleaner."""
    return TextCleaner()


def get_config_loader() -> ConfigLoader:
    """Get config loader."""
    return ConfigLoader()


def get_workflow_repository(db: Session = Depends(get_db)) -> WorkflowRepository:
    """Get workflow repository."""
    return create_workflow_repository(db)


def get_workflow_plugin_config_repository(db: Session = Depends(get_db)) -> WorkflowPluginConfigRepository:
    """Get workflow plugin config repository."""
    return create_workflow_plugin_config_repository(db)


def get_plugin_repository(db: Session = Depends(get_db)) -> PluginRepository:
    """Get plugin repository."""
    return create_plugin_repository(db)


def get_plugin_execution_repository(db: Session = Depends(get_db)) -> PluginExecutionRepository:
    """Get plugin execution repository."""
    return create_plugin_execution_repository(db)


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    """Get project repository (factory selects SQLite or PostgreSQL implementation)."""
    return create_project_repository(db)


def get_project_plugin_config_repository(db: Session = Depends(get_db)) -> ProjectPluginConfigRepository:
    """Get project plugin config repository (factory selects SQLite or PostgreSQL implementation)."""
    return create_project_plugin_config_repository(db)


def get_core_api(
    paper_repository: PaperRepository = Depends(get_paper_repository),
    config_repository: ConfigRepository = Depends(get_config_repository),
    project_plugin_config_repository: ProjectPluginConfigRepository = Depends(get_project_plugin_config_repository),
) -> CoreAPI:
    """Get Core API instance."""
    return CoreAPIImpl(
        paper_repository=paper_repository,
        config_repository=config_repository,
        project_plugin_config_repository=project_plugin_config_repository,
    )


def get_plugin_registry(
    plugin_repository: PluginRepository = Depends(get_plugin_repository),
    core_api: CoreAPI = Depends(get_core_api),
) -> PluginRegistry:
    """Get plugin registry with CoreAPI injection."""
    return PluginRegistry(plugin_repository, PluginLoader(), core_api)


def get_plugin_executor(
    plugin_registry: PluginRegistry = Depends(get_plugin_registry),
    execution_repository: PluginExecutionRepository = Depends(get_plugin_execution_repository),
) -> PluginExecutor:
    """Get plugin executor."""
    return PluginExecutor(plugin_registry, execution_repository)

