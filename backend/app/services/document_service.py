"""Document management service."""

import logging
from pathlib import Path
from typing import List, Optional

import frontmatter

from app.core.config import settings
from app.models.document import Document, DocumentMetadata

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for managing documents."""

    def __init__(self, documents_dir: Path = settings.DOCUMENTS_DIR):
        """Initialize document service.

        Args:
            documents_dir: Directory containing documents
        """
        self.documents_dir = documents_dir
        self.documents_dir.mkdir(parents=True, exist_ok=True)

    def list_documents(self) -> List[dict]:
        """List all documents in the documents directory.

        Returns:
            List of document metadata dictionaries
        """
        documents = []

        for file_path in self.documents_dir.glob("*.md"):
            try:
                doc = self.load_document(file_path.name)
                documents.append(
                    {
                        "filename": doc.filename,
                        "metadata": doc.metadata.model_dump(),
                        "modified": file_path.stat().st_mtime,
                        "size": file_path.stat().st_size,
                    }
                )
            except Exception as e:
                logger.error(f"Error loading document {file_path}: {e}")

        return sorted(documents, key=lambda x: x["modified"], reverse=True)

    def load_document(self, filename: str) -> Document:
        """Load a document from disk.

        Args:
            filename: Name of the document file

        Returns:
            Document object

        Raises:
            FileNotFoundError: If document doesn't exist
        """
        file_path = self.documents_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {filename}")

        # Parse frontmatter and content
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Extract metadata
        metadata = DocumentMetadata(**post.metadata) if post.metadata else DocumentMetadata()

        return Document(
            filename=filename,
            metadata=metadata,
            content=post.content,
            raw_content=frontmatter.dumps(post),
        )

    def save_document(
        self, filename: str, metadata: DocumentMetadata, content: str
    ) -> Document:
        """Save a document to disk.

        Args:
            filename: Name of the document file
            metadata: Document metadata
            content: Markdown content

        Returns:
            Saved document object
        """
        # Ensure filename ends with .md
        if not filename.endswith(".md"):
            filename += ".md"

        file_path = self.documents_dir / filename

        # Create frontmatter post
        post = frontmatter.Post(content)
        # Only include non-None metadata fields
        post.metadata = {
            k: v for k, v in metadata.model_dump().items() if v is not None and k != "extra"
        }
        # Add extra fields
        if metadata.extra:
            post.metadata.update(metadata.extra)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        logger.info(f"Saved document: {filename}")

        return self.load_document(filename)

    def delete_document(self, filename: str) -> bool:
        """Delete a document.

        Args:
            filename: Name of the document file

        Returns:
            True if deleted successfully

        Raises:
            FileNotFoundError: If document doesn't exist
        """
        file_path = self.documents_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {filename}")

        file_path.unlink()
        logger.info(f"Deleted document: {filename}")

        return True

    def document_exists(self, filename: str) -> bool:
        """Check if a document exists.

        Args:
            filename: Name of the document file

        Returns:
            True if document exists
        """
        return (self.documents_dir / filename).exists()


# Singleton instance
document_service = DocumentService()
