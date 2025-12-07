"""
Tests for configuration management
"""

import pytest
import tempfile
from pathlib import Path
from auto_templates.core.config import TemplateConfig


class TestTemplateConfig:
    """Test cases for TemplateConfig"""

    def test_create_default_config(self):
        """Test creating a default configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config = TemplateConfig.create_default_config(str(config_file))

            assert config_file.exists()
            assert config.get("version") == "1.0.0"
            assert "variables" in config.config
            assert "templates" in config.config

    def test_load_config(self):
        """Test loading configuration from file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config_file.write_text(
                """
version: '1.0.0'
variables:
  name: Test
  value: 123
templates: {}
"""
            )

            config = TemplateConfig(str(config_file))
            assert config.get("version") == "1.0.0"
            assert config.get("variables.name") == "Test"
            assert config.get("variables.value") == 123

    def test_get_with_dot_notation(self):
        """Test getting nested values with dot notation"""
        config = TemplateConfig()
        config.config = {"level1": {"level2": {"level3": "value"}}}

        assert config.get("level1.level2.level3") == "value"
        assert config.get("level1.level2") == {"level3": "value"}

    def test_get_with_default(self):
        """Test getting values with default fallback"""
        config = TemplateConfig()
        config.config = {"key": "value"}

        assert config.get("key") == "value"
        assert config.get("nonexistent", "default") == "default"
        assert config.get("nested.key", "default") == "default"

    def test_set_simple_value(self):
        """Test setting a simple value"""
        config = TemplateConfig()
        config.set("key", "value")

        assert config.get("key") == "value"

    def test_set_nested_value(self):
        """Test setting nested values with dot notation"""
        config = TemplateConfig()
        config.set("level1.level2.key", "value")

        assert config.get("level1.level2.key") == "value"
        assert isinstance(config.config["level1"], dict)
        assert isinstance(config.config["level1"]["level2"], dict)

    def test_get_variables(self):
        """Test getting template variables"""
        config = TemplateConfig()
        config.config = {"variables": {"name": "Test", "version": "1.0.0"}}

        variables = config.get_variables()
        assert variables["name"] == "Test"
        assert variables["version"] == "1.0.0"

    def test_get_variables_empty(self):
        """Test getting variables when none exist"""
        config = TemplateConfig()
        variables = config.get_variables()
        assert variables == {}

    def test_add_template(self):
        """Test adding a template definition"""
        config = TemplateConfig()
        config.add_template(
            "my_template", {"file": "template.j2", "description": "Test template"}
        )

        assert "my_template" in config.config["templates"]
        assert config.config["templates"]["my_template"]["file"] == "template.j2"

    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"

            # Create and save config
            config1 = TemplateConfig()
            config1.set("test_key", "test_value")
            config1.set("nested.key", "nested_value")
            config1.save_config(str(config_file))

            # Load config
            config2 = TemplateConfig(str(config_file))
            assert config2.get("test_key") == "test_value"
            assert config2.get("nested.key") == "nested_value"

    def test_load_nonexistent_config(self):
        """Test that loading nonexistent config raises error"""
        with pytest.raises(FileNotFoundError):
            TemplateConfig("/nonexistent/config.yaml")
