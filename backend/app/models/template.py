"""Template data models."""

from typing import Dict, List, Optional

from pydantic import BaseModel


class TemplateMetadata(BaseModel):
    """Template metadata."""

    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    variables: List[str] = []  # List of required variable names


class Template(BaseModel):
    """Complete template model."""

    filename: str
    metadata: TemplateMetadata
    content: str  # Template content


class TemplateRenderRequest(BaseModel):
    """Request to render a template with variables."""

    template_filename: str
    variables: Dict[str, str]


class TemplateList(BaseModel):
    """List of available templates."""

    templates: List[Template]
    count: int
