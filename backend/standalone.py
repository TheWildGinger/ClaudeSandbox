"""Standalone EngiCalc server for bundled executable."""

import logging
import sys
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path
from threading import Timer

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import calculation, document, export, template
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_base_path() -> Path:
    """Get base path for bundled application or development."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys._MEIPASS)
    else:
        # Running in normal Python environment
        return Path(__file__).resolve().parent.parent


def open_browser():
    """Open browser after a short delay."""
    url = f"http://{settings.HOST}:{settings.PORT}"
    logger.info(f"Opening browser at {url}")
    webbrowser.open(url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("=" * 60)
    logger.info("Starting EngiCalc Standalone Server...")
    logger.info("=" * 60)

    base_path = get_base_path()
    logger.info(f"Base path: {base_path}")

    # Use user's home directory for data files
    user_home = Path.home()
    data_dir = user_home / "EngiCalc"

    # Override settings for standalone mode
    settings.DOCUMENTS_DIR = data_dir / "documents"
    settings.TEMPLATES_DIR = data_dir / "templates"
    settings.EXPORTS_DIR = data_dir / "exports"
    settings.IMAGES_DIR = data_dir / "images"

    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Documents: {settings.DOCUMENTS_DIR}")
    logger.info(f"Templates: {settings.TEMPLATES_DIR}")
    logger.info(f"Exports: {settings.EXPORTS_DIR}")

    # Ensure directories exist
    settings.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    settings.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    settings.IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Create a sample document if none exist
    sample_doc = settings.DOCUMENTS_DIR / "example.md"
    if not sample_doc.exists():
        logger.info("Creating sample document...")
        sample_doc.write_text("""---
project: "Sample Project"
engineer: "Your Name"
date: "2025-11-19"
revision: "A"
---

# Welcome to EngiCalc!

## Introduction

This is a sample engineering calculation document. EngiCalc allows you to:
- Write calculations in Python with unit awareness
- Document your engineering work in Markdown
- Export professional PDFs

## Example Calculation

```python
%%calc
# Define a simple beam
L = 5.0 * ureg.meter
w = 10.0 * ureg.kN / ureg.meter

# Calculate maximum moment
M_max = w * L**2 / 8

print(f"Beam length: {L}")
print(f"Distributed load: {w}")
print(f"Maximum moment: {M_max:.2f}")
```

## Conclusion

Edit this document or create a new one to get started!
""")

    logger.info("=" * 60)
    logger.info(f"Server running at http://{settings.HOST}:{settings.PORT}")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 60)

    # Open browser after 1.5 seconds
    Timer(1.5, open_browser).start()

    yield

    logger.info("Shutting down EngiCalc...")


# Create FastAPI app
app = FastAPI(
    title="EngiCalc Standalone",
    description="Engineering calculation tool",
    version="0.1.0",
    lifespan=lifespan,
)

# Include API routers
app.include_router(calculation.router, prefix="/api/calculation", tags=["calculation"])
app.include_router(document.router, prefix="/api/document", tags=["document"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(template.router, prefix="/api/template", tags=["template"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Determine frontend static files location
base_path = get_base_path()
frontend_dist = base_path / "frontend" / "dist"

if frontend_dist.exists():
    logger.info(f"Serving frontend from: {frontend_dist}")

    # Mount static files (CSS, JS, etc.)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    # Serve index.html for all other routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA."""
        # If path starts with /api, /docs, or /health, let FastAPI handle it
        if full_path.startswith(("api/", "docs", "health", "openapi.json")):
            return {"error": "Not found"}

        # Serve index.html for all other paths
        index_file = frontend_dist / "index.html"
        return FileResponse(index_file)
else:
    logger.warning(f"Frontend not found at {frontend_dist}")
    logger.warning("API will be available, but no UI will be served")


if __name__ == "__main__":
    import uvicorn

    # Disable CORS in standalone mode since everything is served from same origin
    settings.CORS_ORIGINS = ["*"]
    settings.DEBUG = False

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
    )
