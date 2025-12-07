"""
Configuration management for templates
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List


class TemplateConfig:
    """
    Configuration manager for templates
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize template configuration

        Args:
            config_file: Path to YAML configuration file
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}

        if config_file:
            self.load_config(config_file)

    def load_config(self, config_file: str) -> None:
        """
        Load configuration from a YAML file

        Args:
            config_file: Path to YAML configuration file
        """
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f) or {}

    def save_config(self, config_file: Optional[str] = None) -> None:
        """
        Save configuration to a YAML file

        Args:
            config_file: Path to save configuration. Uses loaded file if None
        """
        save_path = config_file or self.config_file

        if not save_path:
            raise ValueError("No configuration file specified")

        config_path = Path(save_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value

        Args:
            key: Configuration key (supports dot notation, e.g., 'template.name')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value

        Args:
            key: Configuration key (supports dot notation, e.g., 'template.name')
            value: Value to set
        """
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_variables(self) -> Dict[str, Any]:
        """
        Get template variables from configuration

        Returns:
            Dictionary of template variables
        """
        return self.config.get("variables", {})

    def get_templates(self) -> List[Dict[str, Any]]:
        """
        Get template definitions from configuration

        Returns:
            List of template definitions
        """
        return self.config.get("templates", [])

    def add_template(self, name: str, template_data: Dict[str, Any]) -> None:
        """
        Add a template definition to configuration

        Args:
            name: Template name
            template_data: Template metadata and settings
        """
        if "templates" not in self.config:
            self.config["templates"] = {}

        self.config["templates"][name] = template_data

    @classmethod
    def create_default_config(cls, output_file: str) -> "TemplateConfig":
        """
        Create a default configuration file

        Args:
            output_file: Path where to save the configuration

        Returns:
            TemplateConfig instance with default settings
        """
        default_config = {
            "version": "1.0.0",
            "variables": {
                "author": "Your Name",
                "email": "your.email@example.com",
                "project_name": "my_project",
                "description": "A new project",
            },
            "templates": {},
            "output_dir": "./output",
        }

        config = cls()
        config.config = default_config
        config.config_file = output_file
        config.save_config(output_file)

        return config
