"""
Template Engine - Core template rendering functionality
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound


class TemplateEngine:
    """
    Main template engine for rendering templates with variable substitution
    """

    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the template engine

        Args:
            template_dir: Directory containing templates. If None, uses built-in templates
        """
        self.template_dir = template_dir or self._get_default_template_dir()
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def _get_default_template_dir(self) -> str:
        """Get the default template directory"""
        package_dir = Path(__file__).parent.parent
        return str(package_dir / "templates")

    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Render a template with the given variables

        Args:
            template_name: Name of the template file
            variables: Dictionary of variables to substitute

        Returns:
            Rendered template string

        Raises:
            TemplateNotFound: If template doesn't exist
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**variables)
        except TemplateNotFound:
            raise FileNotFoundError(
                f"Template '{template_name}' not found in {self.template_dir}"
            )

    def render_string(self, template_string: str, variables: Dict[str, Any]) -> str:
        """
        Render a template string with the given variables

        Args:
            template_string: Template content as string
            variables: Dictionary of variables to substitute

        Returns:
            Rendered template string
        """
        template = Template(template_string)
        return template.render(**variables)

    def render_to_file(
        self,
        template_name: str,
        output_path: str,
        variables: Dict[str, Any],
        create_dirs: bool = True,
    ) -> None:
        """
        Render a template and save to a file

        Args:
            template_name: Name of the template file
            output_path: Path where to save the rendered template
            variables: Dictionary of variables to substitute
            create_dirs: Whether to create parent directories if they don't exist
        """
        rendered_content = self.render_template(template_name, variables)

        output_path_obj = Path(output_path)
        if create_dirs:
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_content)

    def list_templates(self) -> List[str]:
        """
        List all available templates

        Returns:
            List of template names
        """
        templates = []
        template_path = Path(self.template_dir)

        if template_path.exists():
            for file_path in template_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(template_path)
                    templates.append(str(relative_path))

        return sorted(templates)

    def template_exists(self, template_name: str) -> bool:
        """
        Check if a template exists

        Args:
            template_name: Name of the template file

        Returns:
            True if template exists, False otherwise
        """
        template_path = Path(self.template_dir) / template_name
        return template_path.exists()
