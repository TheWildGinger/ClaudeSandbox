"""Template API endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from app.models.template import Template, TemplateList, TemplateRenderRequest
from app.services.template_service import template_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", response_model=TemplateList)
async def list_templates() -> TemplateList:
    """List all available templates.

    Returns:
        List of templates
    """
    try:
        templates = template_service.list_templates()
        return TemplateList(templates=templates, count=len(templates))
    except Exception as e:
        logger.error(f"Error listing templates: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")


@router.get("/{filename}", response_model=Template)
async def get_template(filename: str) -> Template:
    """Get a specific template.

    Args:
        filename: Name of the template file

    Returns:
        Template object
    """
    try:
        return template_service.load_template(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template not found: {filename}")
    except Exception as e:
        logger.error(f"Error loading template {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to load template: {str(e)}")


@router.post("/render")
async def render_template(request: TemplateRenderRequest) -> dict:
    """Render a template with provided variables.

    Args:
        request: Template render request

    Returns:
        Rendered template content
    """
    try:
        rendered_content = template_service.render_template(
            request.template_filename, request.variables
        )
        return {"content": rendered_content}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Template not found: {request.template_filename}"
        )
    except Exception as e:
        logger.error(f"Error rendering template: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to render template: {str(e)}")
