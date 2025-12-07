"""
Tests for the template engine
"""

import pytest
import tempfile
from pathlib import Path
from auto_templates.core.engine import TemplateEngine


class TestTemplateEngine:
    """Test cases for TemplateEngine"""

    def test_render_string_simple(self):
        """Test rendering a simple template string"""
        engine = TemplateEngine()
        result = engine.render_string("Hello {{ name }}!", {"name": "World"})
        assert result == "Hello World!"

    def test_render_string_multiple_variables(self):
        """Test rendering with multiple variables"""
        engine = TemplateEngine()
        template = "{{ greeting }} {{ name }}! You are {{ age }} years old."
        variables = {"greeting": "Hi", "name": "Alice", "age": 25}
        result = engine.render_string(template, variables)
        assert result == "Hi Alice! You are 25 years old."

    def test_render_string_with_conditionals(self):
        """Test rendering with conditionals"""
        engine = TemplateEngine()
        template = "{% if show %}Visible{% else %}Hidden{% endif %}"

        result1 = engine.render_string(template, {"show": True})
        assert result1 == "Visible"

        result2 = engine.render_string(template, {"show": False})
        assert result2 == "Hidden"

    def test_render_string_with_loops(self):
        """Test rendering with loops"""
        engine = TemplateEngine()
        template = "{% for item in items %}- {{ item }}\n{% endfor %}"
        variables = {"items": ["apple", "banana", "orange"]}
        result = engine.render_string(template, variables)
        assert "- apple" in result
        assert "- banana" in result
        assert "- orange" in result

    def test_render_string_with_filters(self):
        """Test rendering with Jinja2 filters"""
        engine = TemplateEngine()

        # Test upper filter
        result1 = engine.render_string("{{ name | upper }}", {"name": "test"})
        assert result1 == "TEST"

        # Test default filter
        result2 = engine.render_string("{{ value | default('N/A') }}", {})
        assert result2 == "N/A"

    def test_render_to_file(self):
        """Test rendering to a file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple template
            template_dir = Path(tmpdir) / "templates"
            template_dir.mkdir()

            template_file = template_dir / "test.j2"
            template_file.write_text("Hello {{ name }}!")

            # Render to output file
            output_file = Path(tmpdir) / "output.txt"
            engine = TemplateEngine(str(template_dir))
            engine.render_to_file("test.j2", str(output_file), {"name": "World"})

            # Verify output
            assert output_file.exists()
            assert output_file.read_text() == "Hello World!"

    def test_render_to_file_creates_directories(self):
        """Test that render_to_file creates parent directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create template
            template_dir = Path(tmpdir) / "templates"
            template_dir.mkdir()

            template_file = template_dir / "test.j2"
            template_file.write_text("Test content")

            # Render to nested path
            output_file = Path(tmpdir) / "nested" / "path" / "output.txt"
            engine = TemplateEngine(str(template_dir))
            engine.render_to_file("test.j2", str(output_file), {})

            assert output_file.exists()
            assert output_file.read_text() == "Test content"

    def test_list_templates(self):
        """Test listing available templates"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_dir = Path(tmpdir)

            # Create some test templates
            (template_dir / "test1.j2").write_text("Template 1")
            (template_dir / "test2.j2").write_text("Template 2")

            subdir = template_dir / "subdir"
            subdir.mkdir()
            (subdir / "test3.j2").write_text("Template 3")

            engine = TemplateEngine(str(template_dir))
            templates = engine.list_templates()

            assert "test1.j2" in templates
            assert "test2.j2" in templates
            assert str(Path("subdir") / "test3.j2") in templates

    def test_template_exists(self):
        """Test checking if template exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_dir = Path(tmpdir)
            (template_dir / "exists.j2").write_text("Exists")

            engine = TemplateEngine(str(template_dir))

            assert engine.template_exists("exists.j2")
            assert not engine.template_exists("notexists.j2")

    def test_template_not_found_error(self):
        """Test that FileNotFoundError is raised for missing templates"""
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = TemplateEngine(tmpdir)

            with pytest.raises(FileNotFoundError):
                engine.render_template("nonexistent.j2", {})
