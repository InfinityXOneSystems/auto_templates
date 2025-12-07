"""
Tests for template loader
"""

import tempfile
from pathlib import Path
from auto_templates.core.loader import TemplateLoader


class TestTemplateLoader:
    """Test cases for TemplateLoader"""

    def test_find_template(self):
        """Test finding a template in search paths"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_dir = Path(tmpdir)
            template_file = template_dir / "test.j2"
            template_file.write_text("Test template")

            loader = TemplateLoader([str(template_dir)])
            found_path = loader.find_template("test.j2")

            assert found_path is not None
            assert Path(found_path).exists()

    def test_find_template_not_found(self):
        """Test finding a template that doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = TemplateLoader([tmpdir])
            found_path = loader.find_template("nonexistent.j2")

            assert found_path is None

    def test_add_search_path(self):
        """Test adding a search path"""
        loader = TemplateLoader()
        initial_count = len(loader.search_paths)

        loader.add_search_path("/some/path")

        assert len(loader.search_paths) == initial_count + 1
        assert "/some/path" in loader.search_paths

    def test_add_search_path_no_duplicates(self):
        """Test that duplicate search paths are not added"""
        loader = TemplateLoader()
        path = "/some/path"

        loader.add_search_path(path)
        count_after_first = len(loader.search_paths)

        loader.add_search_path(path)
        count_after_second = len(loader.search_paths)

        assert count_after_first == count_after_second

    def test_list_all_templates(self):
        """Test listing all templates from all search paths"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create first template directory
            dir1 = Path(tmpdir) / "dir1"
            dir1.mkdir()
            (dir1 / "template1.j2").write_text("Template 1")

            # Create second template directory
            dir2 = Path(tmpdir) / "dir2"
            dir2.mkdir()
            (dir2 / "template2.j2").write_text("Template 2")

            loader = TemplateLoader([str(dir1), str(dir2)])
            all_templates = loader.list_all_templates()

            assert str(dir1) in all_templates
            assert str(dir2) in all_templates
            assert "template1.j2" in all_templates[str(dir1)]
            assert "template2.j2" in all_templates[str(dir2)]

    def test_list_templates_nested(self):
        """Test listing templates with nested directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_dir = Path(tmpdir)

            # Create nested structure
            (template_dir / "template1.j2").write_text("Template 1")
            subdir = template_dir / "subdir"
            subdir.mkdir()
            (subdir / "template2.j2").write_text("Template 2")

            loader = TemplateLoader([str(template_dir)])
            templates = loader._list_templates_in_path(str(template_dir))

            assert "template1.j2" in templates
            assert str(Path("subdir") / "template2.j2") in templates

    def test_get_template_info(self):
        """Test getting information about a template"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_dir = Path(tmpdir)
            template_file = template_dir / "test.j2"
            template_file.write_text("Test content")

            loader = TemplateLoader([str(template_dir)])
            info = loader.get_template_info("test.j2")

            assert info is not None
            assert info["name"] == "test.j2"
            assert info["path"] == str(template_file)
            assert info["size"] > 0
            assert "modified" in info

    def test_get_template_info_not_found(self):
        """Test getting info for nonexistent template"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = TemplateLoader([tmpdir])
            info = loader.get_template_info("nonexistent.j2")

            assert info is None
