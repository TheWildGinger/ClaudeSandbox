"""Template management service."""

import logging
import re
from pathlib import Path
from typing import Dict, List

import frontmatter
from jinja2 import Template as Jinja2Template

from app.core.config import settings
from app.models.template import Template, TemplateMetadata

logger = logging.getLogger(__name__)


class TemplateService:
    """Service for managing calculation templates."""

    def __init__(self, templates_dir: Path = settings.TEMPLATES_DIR):
        """Initialize template service.

        Args:
            templates_dir: Directory containing templates
        """
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def list_templates(self) -> List[Template]:
        """List all available templates.

        Returns:
            List of Template objects
        """
        templates = []

        for file_path in self.templates_dir.glob("*.md"):
            try:
                template = self.load_template(file_path.name)
                templates.append(template)
            except Exception as e:
                logger.error(f"Error loading template {file_path}: {e}")

        return sorted(templates, key=lambda x: x.metadata.name)

    def load_template(self, filename: str) -> Template:
        """Load a template from disk.

        Args:
            filename: Name of the template file

        Returns:
            Template object

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        file_path = self.templates_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Template not found: {filename}")

        # Parse frontmatter and content
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Extract metadata
        metadata_dict = post.metadata if post.metadata else {}

        # Extract variables from template content
        variables = self._extract_variables(post.content)

        metadata = TemplateMetadata(
            name=metadata_dict.get("name", filename.replace(".md", "")),
            description=metadata_dict.get("description"),
            category=metadata_dict.get("category"),
            variables=metadata_dict.get("variables", variables),
        )

        return Template(filename=filename, metadata=metadata, content=post.content)

    def render_template(self, filename: str, variables: Dict[str, str]) -> str:
        """Render a template with provided variables.

        Args:
            filename: Name of the template file
            variables: Dictionary of variable name -> value

        Returns:
            Rendered template content
        """
        template = self.load_template(filename)

        # Use Jinja2 for rendering
        jinja_template = Jinja2Template(template.content)
        rendered_content = jinja_template.render(**variables)

        return rendered_content

    def _extract_variables(self, content: str) -> List[str]:
        """Extract variable placeholders from template content.

        Args:
            content: Template content

        Returns:
            List of unique variable names
        """
        # Find all {{variable_name}} patterns
        pattern = settings.TEMPLATE_VARIABLES_PATTERN
        matches = re.findall(pattern, content)

        # Return unique variable names
        return sorted(set(matches))


# Singleton instance
template_service = TemplateService()
