"""Export service for generating PDFs and other formats."""

import logging
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class ExportService:
    """Service for exporting documents to various formats."""

    def __init__(self, exports_dir: Path = settings.EXPORTS_DIR):
        """Initialize export service.

        Args:
            exports_dir: Directory for exported files
        """
        self.exports_dir = exports_dir
        self.exports_dir.mkdir(parents=True, exist_ok=True)

        # Check if pandoc is available
        self.pandoc_available = shutil.which(settings.PANDOC_PATH) is not None
        if not self.pandoc_available:
            logger.warning("Pandoc not found - PDF export will not be available")

    def export_to_pdf(
        self, markdown_content: str, output_filename: str, metadata: Optional[dict] = None
    ) -> Path:
        """Export markdown content to PDF using Pandoc.

        Args:
            markdown_content: The markdown content to export
            output_filename: Desired output filename (without extension)
            metadata: Optional metadata for the PDF

        Returns:
            Path to the generated PDF file

        Raises:
            RuntimeError: If Pandoc is not available or export fails
        """
        if not self.pandoc_available:
            raise RuntimeError("Pandoc is not available. Please install Pandoc for PDF export.")

        # Ensure output filename ends with .pdf
        if not output_filename.endswith(".pdf"):
            output_filename += ".pdf"

        output_path = self.exports_dir / output_filename

        # Create temporary markdown file
        temp_md_path = self.exports_dir / f"temp_{datetime.now().timestamp()}.md"

        try:
            # Write markdown content to temp file
            with open(temp_md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            # Build pandoc command
            pandoc_cmd = [
                settings.PANDOC_PATH,
                str(temp_md_path),
                "-o",
                str(output_path),
                "--pdf-engine=" + settings.PDF_ENGINE,
                "--standalone",
                # Add nice styling
                "-V",
                "geometry:margin=1in",
                "-V",
                "fontsize=11pt",
                # Enable math
                "--mathjax",
            ]

            # Add metadata if provided
            if metadata:
                if "title" in metadata:
                    pandoc_cmd.extend(["-V", f"title={metadata['title']}"])
                if "author" in metadata or "engineer" in metadata:
                    author = metadata.get("author") or metadata.get("engineer")
                    pandoc_cmd.extend(["-V", f"author={author}"])
                if "date" in metadata:
                    pandoc_cmd.extend(["-V", f"date={metadata['date']}"])

            # Execute pandoc
            result = subprocess.run(
                pandoc_cmd, capture_output=True, text=True, timeout=60  # 60 second timeout
            )

            if result.returncode != 0:
                error_msg = f"Pandoc export failed: {result.stderr}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            logger.info(f"Successfully exported PDF: {output_path}")
            return output_path

        except subprocess.TimeoutExpired:
            raise RuntimeError("PDF export timed out after 60 seconds")

        except Exception as e:
            logger.error(f"PDF export error: {e}", exc_info=True)
            raise RuntimeError(f"PDF export failed: {str(e)}")

        finally:
            # Clean up temp file
            if temp_md_path.exists():
                temp_md_path.unlink()

    def export_to_html(self, markdown_content: str, output_filename: str) -> Path:
        """Export markdown content to HTML.

        Args:
            markdown_content: The markdown content to export
            output_filename: Desired output filename (without extension)

        Returns:
            Path to the generated HTML file
        """
        # Ensure output filename ends with .html
        if not output_filename.endswith(".html"):
            output_filename += ".html"

        output_path = self.exports_dir / output_filename

        # For MVP, simple HTML wrapper
        # In production, would use a proper HTML template with CSS
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engineering Calculation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body);"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
        pre {{
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
{markdown_content}
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"Successfully exported HTML: {output_path}")
        return output_path


# Singleton instance
export_service = ExportService()
