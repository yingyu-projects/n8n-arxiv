"""Project repository implementation for SQLite."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.domain.project.repositories.project_repository import ProjectRepository
from app.domain.project.entities.project import Project
from app.infrastructure.database.models.project_orm import ProjectORM
from app.infrastructure.mappers.project_mapper import ProjectMapper


class ProjectRepositorySQLite(ProjectRepository):
    """SQLite-specific implementation of ProjectRepository."""
    
    def __init__(self, session: Session):
        """Initialize with database session."""
        self._session = session
    
    async def save(self, project: Project) -> Project:
        """Save a project."""
        project_id = str(project.id)
        existing = self._session.query(ProjectORM).filter(
            ProjectORM.id == project_id
        ).first()
        
        if existing:
            ProjectMapper.update_orm_from_domain(existing, project)
            self._session.commit()
            self._session.refresh(existing)
            return ProjectMapper.to_domain(existing)
        else:
            orm = ProjectMapper.to_orm(project, convert_uuid_to_string=True)
            self._session.add(orm)
            self._session.commit()
            self._session.refresh(orm)
            return ProjectMapper.to_domain(orm)
    
    async def find_by_id(self, project_id: UUID) -> Optional[Project]:
        """Find project by ID."""
        query_id = str(project_id)
        orm = self._session.query(ProjectORM).filter(
            ProjectORM.id == query_id
        ).first()
        
        return ProjectMapper.to_domain(orm) if orm else None
    
    async def find_by_name(self, name: str) -> Optional[Project]:
        """Find project by name."""
        orm = self._session.query(ProjectORM).filter(
            ProjectORM.name == name
        ).first()
        
        return ProjectMapper.to_domain(orm) if orm else None
    
    async def find_all(self) -> List[Project]:
        """Find all projects."""
        query = self._session.query(ProjectORM)
        query = query.order_by(ProjectORM.created_at.desc())
        orms = query.all()
        return [ProjectMapper.to_domain(orm) for orm in orms]
    
    async def delete(self, project_id: UUID) -> None:
        """Delete a project."""
        query_id = str(project_id)
        orm = self._session.query(ProjectORM).filter(
            ProjectORM.id == query_id
        ).first()
        
        if orm:
            self._session.delete(orm)
            self._session.commit()


