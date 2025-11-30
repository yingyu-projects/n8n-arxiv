"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.presentation.api import papers, categories, workflow


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
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


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "arXiv Parser API", "version": settings.api_version}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

