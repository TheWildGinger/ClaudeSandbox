"""Document API endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from app.models.document import Document, DocumentCreate, DocumentList, DocumentUpdate
from app.services.document_service import document_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", response_model=DocumentList)
async def list_documents() -> DocumentList:
    """List all documents.

    Returns:
        List of documents with metadata
    """
    try:
        documents = document_service.list_documents()
        return DocumentList(documents=documents, count=len(documents))
    except Exception as e:
        logger.error(f"Error listing documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")


@router.get("/{filename}", response_model=Document)
async def get_document(filename: str) -> Document:
    """Get a specific document.

    Args:
        filename: Name of the document file

    Returns:
        Document object
    """
    try:
        return document_service.load_document(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Document not found: {filename}")
    except Exception as e:
        logger.error(f"Error loading document {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to load document: {str(e)}")


@router.post("/create", response_model=Document)
async def create_document(doc: DocumentCreate) -> Document:
    """Create a new document.

    Args:
        doc: Document creation request

    Returns:
        Created document
    """
    try:
        # Check if document already exists
        if document_service.document_exists(doc.filename):
            raise HTTPException(status_code=409, detail=f"Document already exists: {doc.filename}")

        return document_service.save_document(doc.filename, doc.metadata, doc.content)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create document: {str(e)}")


@router.put("/{filename}", response_model=Document)
async def update_document(filename: str, update: DocumentUpdate) -> Document:
    """Update an existing document.

    Args:
        filename: Name of the document file
        update: Document update request

    Returns:
        Updated document
    """
    try:
        # Load existing document
        existing_doc = document_service.load_document(filename)

        # Update metadata if provided
        metadata = update.metadata if update.metadata else existing_doc.metadata

        # Update content if provided
        content = update.content if update.content is not None else existing_doc.content

        return document_service.save_document(filename, metadata, content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Document not found: {filename}")
    except Exception as e:
        logger.error(f"Error updating document {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update document: {str(e)}")


@router.delete("/{filename}")
async def delete_document(filename: str) -> dict:
    """Delete a document.

    Args:
        filename: Name of the document file

    Returns:
        Success message
    """
    try:
        document_service.delete_document(filename)
        return {"message": f"Document deleted: {filename}"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Document not found: {filename}")
    except Exception as e:
        logger.error(f"Error deleting document {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
