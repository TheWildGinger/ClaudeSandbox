"""Document data models."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Document metadata from YAML frontmatter."""

    project: Optional[str] = None
    engineer: Optional[str] = None
    date: Optional[str] = None
    revision: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    # Allow additional fields
    extra: Dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    """Complete document model."""

    filename: str
    metadata: DocumentMetadata
    content: str  # Markdown content without frontmatter
    raw_content: str  # Full content including frontmatter


class DocumentCreate(BaseModel):
    """Request model for creating a document."""

    filename: str
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    content: str = ""


class DocumentUpdate(BaseModel):
    """Request model for updating a document."""

    metadata: Optional[DocumentMetadata] = None
    content: Optional[str] = None


class DocumentList(BaseModel):
    """List of documents."""

    documents: list[Dict[str, Any]]
    count: int
