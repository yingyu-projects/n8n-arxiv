"""Mapper between Project ORM and Domain entity."""
import uuid

from app.domain.project.entities.project import Project
from app.infrastructure.database.models.project_orm import ProjectORM


class ProjectMapper:
    """Mapper for converting between Project ORM and Domain entity."""
    
    @staticmethod
    def _ensure_uuid(id_value) -> uuid.UUID:
        """Convert string UUID to UUID object if needed (for SQLite)."""
        if isinstance(id_value, str):
            return uuid.UUID(id_value)
        return id_value
    
    @staticmethod
    def to_domain(orm: ProjectORM) -> Project:
        """Convert ORM model to domain entity."""
        return Project(
            id=ProjectMapper._ensure_uuid(orm.id),
            name=orm.name,
            description=orm.description,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
    
    @staticmethod
    def to_orm(domain: Project, convert_uuid_to_string: bool = False) -> ProjectORM:
        """Convert domain entity to ORM model.
        
        Args:
            domain: Domain entity to convert
            convert_uuid_to_string: If True, convert UUID to string (for SQLite)
        """
        project_id = str(domain.id) if convert_uuid_to_string else domain.id
        
        return ProjectORM(
            id=project_id,
            name=domain.name,
            description=domain.description,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
    
    @staticmethod
    def update_orm_from_domain(orm: ProjectORM, domain: Project) -> None:
        """Update ORM model from domain entity."""
        orm.name = domain.name
        orm.description = domain.description
        orm.updated_at = domain.updated_at


