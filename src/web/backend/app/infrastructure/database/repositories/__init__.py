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

# Import repository interfaces
from app.domain.paper.repositories.paper_repository import PaperRepository
from app.domain.category.repositories.category_repository import CategoryRepository
from app.domain.config.repositories.config_repository import ConfigRepository


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
