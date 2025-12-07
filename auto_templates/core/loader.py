"""
Template loader for managing template discovery and loading
"""

from pathlib import Path
from typing import List, Dict, Any, Optional


class TemplateLoader:
    """
    Manages template discovery and loading from various sources
    """

    def __init__(self, search_paths: Optional[List[str]] = None):
        """
        Initialize the template loader

        Args:
            search_paths: List of directories to search for templates
        """
        self.search_paths = search_paths or []
        self._add_default_paths()

    def _add_default_paths(self) -> None:
        """Add default template search paths"""
        # Add package templates directory
        package_dir = Path(__file__).parent.parent
        default_template_dir = package_dir / "templates"
        if str(default_template_dir) not in self.search_paths:
            self.search_paths.insert(0, str(default_template_dir))

        # Add user templates directory
        user_template_dir = Path.home() / ".auto_templates" / "templates"
        if (
            str(user_template_dir) not in self.search_paths
            and user_template_dir.exists()
        ):
            self.search_paths.insert(0, str(user_template_dir))

    def add_search_path(self, path: str) -> None:
        """
        Add a search path for templates

        Args:
            path: Directory path to add
        """
        if path not in self.search_paths:
            self.search_paths.insert(0, path)

    def find_template(self, template_name: str) -> Optional[str]:
        """
        Find a template in search paths

        Args:
            template_name: Name of the template to find

        Returns:
            Full path to template if found, None otherwise
        """
        for search_path in self.search_paths:
            template_path = Path(search_path) / template_name
            if template_path.exists() and template_path.is_file():
                return str(template_path)

        return None

    def list_all_templates(self) -> Dict[str, List[str]]:
        """
        List all templates from all search paths

        Returns:
            Dictionary mapping search paths to lists of templates
        """
        all_templates = {}

        for search_path in self.search_paths:
            templates = self._list_templates_in_path(search_path)
            if templates:
                all_templates[search_path] = templates

        return all_templates

    def _list_templates_in_path(self, path: str) -> List[str]:
        """
        List templates in a specific path

        Args:
            path: Directory path to search

        Returns:
            List of template names
        """
        templates = []
        path_obj = Path(path)

        if not path_obj.exists():
            return templates

        for file_path in path_obj.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                relative_path = file_path.relative_to(path_obj)
                templates.append(str(relative_path))

        return sorted(templates)

    def get_template_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a template

        Args:
            template_name: Name of the template

        Returns:
            Dictionary with template information or None if not found
        """
        template_path = self.find_template(template_name)

        if not template_path:
            return None

        path_obj = Path(template_path)

        return {
            "name": template_name,
            "path": template_path,
            "size": path_obj.stat().st_size,
            "modified": path_obj.stat().st_mtime,
        }
