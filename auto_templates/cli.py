"""
Command-line interface for auto templates
"""

import sys
import click
from pathlib import Path
from typing import Optional

from auto_templates.core.engine import TemplateEngine
from auto_templates.core.config import TemplateConfig
from auto_templates.core.loader import TemplateLoader


@click.group()
@click.version_option(version="1.0.0", prog_name="auto-templates")
def main():
    """
    Auto Templates - A comprehensive auto-templating system

    Generate files and projects from templates with ease.
    """
    pass


@main.command()
@click.argument("template_name")
@click.argument("output_path")
@click.option("--config", "-c", help="Configuration file with variables")
@click.option("--var", "-v", multiple=True, help="Variables in KEY=VALUE format")
@click.option("--template-dir", "-t", help="Custom template directory")
def generate(
    template_name: str,
    output_path: str,
    config: Optional[str],
    var: tuple,
    template_dir: Optional[str],
):
    """
    Generate a file from a template

    TEMPLATE_NAME: Name of the template to use
    OUTPUT_PATH: Where to save the generated file

    Examples:

        auto-templates generate python/class.py.j2 myclass.py -v name=MyClass

        auto-templates generate readme.md.j2 README.md -c config.yaml
    """
    try:
        # Load configuration if provided
        variables = {}
        if config:
            template_config = TemplateConfig(config)
            variables = template_config.get_variables()

        # Parse command-line variables
        for var_str in var:
            if "=" in var_str:
                key, value = var_str.split("=", 1)
                variables[key.strip()] = value.strip()
            else:
                click.echo(
                    f"Warning: Ignoring invalid variable format: {var_str}", err=True
                )

        # Initialize engine and render
        engine = TemplateEngine(template_dir)
        engine.render_to_file(template_name, output_path, variables)

        click.echo(f"✓ Successfully generated: {output_path}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error generating file: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--template-dir", "-t", help="Custom template directory to list")
def list_templates(template_dir: Optional[str]):
    """
    List all available templates

    Examples:

        auto-templates list

        auto-templates list -t /path/to/templates
    """
    try:
        if template_dir:
            engine = TemplateEngine(template_dir)
            templates = engine.list_templates()
            click.echo(f"\nTemplates in {template_dir}:")
        else:
            loader = TemplateLoader()
            all_templates = loader.list_all_templates()

            if not all_templates:
                click.echo("No templates found.")
                return

            for path, templates in all_templates.items():
                click.echo(f"\nTemplates in {path}:")
                for template in templates:
                    click.echo(f"  - {template}")
            return

        if not templates:
            click.echo("No templates found.")
        else:
            for template in templates:
                click.echo(f"  - {template}")

    except Exception as e:
        click.echo(f"Error listing templates: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("output_file", default="auto_templates.yaml")
def init(output_file: str):
    """
    Initialize a new configuration file

    OUTPUT_FILE: Path to save configuration (default: auto_templates.yaml)

    Examples:

        auto-templates init

        auto-templates init myconfig.yaml
    """
    try:
        if Path(output_file).exists():
            if not click.confirm(f"{output_file} already exists. Overwrite?"):
                click.echo("Aborted.")
                return

        TemplateConfig.create_default_config(output_file)
        click.echo(f"✓ Created configuration file: {output_file}")
        click.echo("\nEdit this file to customize your template variables.")

    except Exception as e:
        click.echo(f"Error creating configuration: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("template_name")
@click.option("--template-dir", "-t", help="Custom template directory")
def show(template_name: str, template_dir: Optional[str]):
    """
    Show the content of a template

    TEMPLATE_NAME: Name of the template to display

    Examples:

        auto-templates show python/class.py.j2
    """
    try:
        loader = TemplateLoader()
        if template_dir:
            loader.add_search_path(template_dir)

        template_path = loader.find_template(template_name)

        if not template_path:
            click.echo(f"Error: Template '{template_name}' not found", err=True)
            sys.exit(1)

        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        click.echo(f"\n=== {template_name} ===\n")
        click.echo(content)

    except Exception as e:
        click.echo(f"Error showing template: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("template_string")
@click.option("--var", "-v", multiple=True, help="Variables in KEY=VALUE format")
@click.option("--config", "-c", help="Configuration file with variables")
def render(template_string: str, var: tuple, config: Optional[str]):
    """
    Render a template string directly

    TEMPLATE_STRING: Template string to render

    Examples:

        auto-templates render "Hello {{ name }}!" -v name=World

        auto-templates render "Project: {{ project }}" -c config.yaml
    """
    try:
        # Load configuration if provided
        variables = {}
        if config:
            template_config = TemplateConfig(config)
            variables = template_config.get_variables()

        # Parse command-line variables
        for var_str in var:
            if "=" in var_str:
                key, value = var_str.split("=", 1)
                variables[key.strip()] = value.strip()

        # Render template
        engine = TemplateEngine()
        result = engine.render_string(template_string, variables)

        click.echo(result)

    except Exception as e:
        click.echo(f"Error rendering template: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
