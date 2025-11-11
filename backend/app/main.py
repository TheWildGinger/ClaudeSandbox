"""Main FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import calculation, document, export, template
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting EngiCalc backend...")
    logger.info(f"Documents directory: {settings.DOCUMENTS_DIR}")
    logger.info(f"Templates directory: {settings.TEMPLATES_DIR}")
    logger.info(f"Exports directory: {settings.EXPORTS_DIR}")

    # Ensure directories exist
    settings.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    settings.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    yield

    logger.info("Shutting down EngiCalc backend...")


# Create FastAPI app
app = FastAPI(
    title="EngiCalc API",
    description="Engineering calculation tool backend API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(calculation.router, prefix="/api/calculation", tags=["calculation"])
app.include_router(document.router, prefix="/api/document", tags=["document"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(template.router, prefix="/api/template", tags=["template"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "EngiCalc API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
