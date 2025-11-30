"""SQLAlchemy database setup."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Determine if using SQLite from explicit database type configuration
is_sqlite = settings.database_type == "sqlite"

# Create engine with appropriate settings
if is_sqlite:
    # SQLite-specific settings
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},  # Required for SQLite
        echo=False,
    )
else:
    # PostgreSQL settings
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        echo=False,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

