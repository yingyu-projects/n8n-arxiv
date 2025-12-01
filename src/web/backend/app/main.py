"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.presentation.api import papers, categories, workflow, config, workflows, plugins, projects
from app.infrastructure.database.database import SessionLocal
from app.infrastructure.database.repositories import (
    create_plugin_repository,
)
from app.application.plugin.plugin_registry import PluginRegistry
from app.infrastructure.plugin.plugin_loader import PluginLoader


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup: Auto-discover and register plugins
    try:
        db = SessionLocal()
        try:
            plugin_repository = create_plugin_repository(db)
            plugin_registry = PluginRegistry(plugin_repository, PluginLoader())
            registered = await plugin_registry.discover_and_register_plugins()
            print(f"Auto-discovered and registered {len(registered)} plugins on startup")
        finally:
            db.close()
    except Exception as e:
        print(f"Warning: Failed to auto-discover plugins on startup: {e}")
    
    yield
    
    # Shutdown (if needed)
    pass


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(papers.router, prefix=settings.api_prefix, tags=["papers"])
app.include_router(categories.router, prefix=settings.api_prefix, tags=["categories"])
app.include_router(workflow.router, prefix=settings.api_prefix, tags=["workflow"])
app.include_router(config.router, prefix=settings.api_prefix, tags=["config"])
app.include_router(workflows.router, prefix=settings.api_prefix, tags=["workflows"])
app.include_router(plugins.router, prefix=settings.api_prefix, tags=["plugins"])
app.include_router(projects.router, prefix=settings.api_prefix, tags=["projects"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "arXiv Parser API", "version": settings.api_version}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

