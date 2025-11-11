"""Export API endpoints."""

import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.export_service import export_service

logger = logging.getLogger(__name__)

router = APIRouter()


class ExportRequest(BaseModel):
    """Request model for exporting documents."""

    markdown_content: str
    output_filename: str
    metadata: dict | None = None


@router.post("/pdf")
async def export_pdf(request: ExportRequest) -> FileResponse:
    """Export markdown content to PDF.

    Args:
        request: Export request with content and filename

    Returns:
        PDF file response
    """
    try:
        pdf_path = export_service.export_to_pdf(
            request.markdown_content, request.output_filename, request.metadata
        )

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=pdf_path.name,
        )

    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"PDF export error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.post("/html")
async def export_html(request: ExportRequest) -> FileResponse:
    """Export markdown content to HTML.

    Args:
        request: Export request with content and filename

    Returns:
        HTML file response
    """
    try:
        html_path = export_service.export_to_html(request.markdown_content, request.output_filename)

        return FileResponse(
            path=html_path,
            media_type="text/html",
            filename=html_path.name,
        )

    except Exception as e:
        logger.error(f"HTML export error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"HTML export failed: {str(e)}")


@router.get("/check-pandoc")
async def check_pandoc() -> dict:
    """Check if Pandoc is available.

    Returns:
        Status of Pandoc availability
    """
    return {
        "available": export_service.pandoc_available,
        "message": "Pandoc is available"
        if export_service.pandoc_available
        else "Pandoc is not installed. PDF export will not work.",
    }
