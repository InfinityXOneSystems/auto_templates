# Auto Templates

A comprehensive auto-templating system for generating files and projects from templates with ease.

## Features

- 🚀 **Powerful Template Engine**: Built on Jinja2 for flexible template rendering
- 📦 **Built-in Templates**: Ready-to-use templates for Python, HTML, configurations, and documentation
- ⚙️ **Configuration Management**: YAML-based configuration for template variables
- 🔧 **CLI Interface**: Easy-to-use command-line tool
- 🎯 **Variable Substitution**: Dynamic content generation with template variables
- 📚 **Extensible**: Add your own custom templates
- 🔍 **Template Discovery**: Automatic template loading from multiple directories

## Installation

### From Source

```bash
git clone https://github.com/InfinityXOneSystems/auto_templates.git
cd auto_templates
pip install -e .
```

### Using pip (when published)

```bash
pip install auto_templates
```

## Quick Start

### 1. Initialize a Configuration File

```bash
auto-templates init
```

This creates an `auto_templates.yaml` file with default variables.

### 2. List Available Templates

```bash
auto-templates list
```

### 3. Generate Files from Templates

Generate a Python class:

```bash
auto-templates generate python/class.py.j2 output.py \
  -v name=MyClass \
  -v description="My awesome class"
```

Generate with a configuration file:

```bash
auto-templates generate docs/README.md.j2 README.md -c auto_templates.yaml
```

### 4. Render Template Strings

```bash
auto-templates render "Hello {{ name }}!" -v name=World
```

## Usage

### Command-Line Interface

#### `generate` - Generate files from templates

```bash
auto-templates generate TEMPLATE_NAME OUTPUT_PATH [OPTIONS]

Options:
  -c, --config FILE       Configuration file with variables
  -v, --var KEY=VALUE     Template variables (can be used multiple times)
  -t, --template-dir DIR  Custom template directory
```

**Examples:**

```bash
# Generate a Python class with inline variables
auto-templates generate python/class.py.j2 myclass.py \
  -v name=UserManager \
  -v author="John Doe" \
  -v description="User management class"

# Generate using a config file
auto-templates generate web/html5.html.j2 index.html -c config.yaml

# Use custom template directory
auto-templates generate mytemplate.j2 output.txt -t ./my_templates/
```

#### `list` - List available templates

```bash
auto-templates list [OPTIONS]

Options:
  -t, --template-dir DIR  Custom template directory to list
```

#### `init` - Initialize configuration file

```bash
auto-templates init [OUTPUT_FILE]
```

Creates a new configuration file with default values.

#### `show` - Display template content

```bash
auto-templates show TEMPLATE_NAME [OPTIONS]

Options:
  -t, --template-dir DIR  Custom template directory
```

#### `render` - Render template strings

```bash
auto-templates render TEMPLATE_STRING [OPTIONS]

Options:
  -v, --var KEY=VALUE     Template variables
  -c, --config FILE       Configuration file with variables
```

### Python API

```python
from auto_templates import TemplateEngine, TemplateConfig

# Using the template engine directly
engine = TemplateEngine()
result = engine.render_template('python/class.py.j2', {
    'name': 'MyClass',
    'description': 'A sample class'
})
print(result)

# Using configuration
config = TemplateConfig('config.yaml')
variables = config.get_variables()
engine.render_to_file('docs/README.md.j2', 'README.md', variables)
```

## Built-in Templates

### Python Templates

- `python/class.py.j2` - Python class template
- `python/function.py.j2` - Python function template
- `python/module.py.j2` - Python module template

### Web Templates

- `web/html5.html.j2` - HTML5 page template

### Configuration Templates

- `config/gitignore.j2` - .gitignore file template

### Documentation Templates

- `docs/README.md.j2` - README.md template
- `docs/LICENSE.j2` - LICENSE file template

## Creating Custom Templates

Templates use Jinja2 syntax. Create a `.j2` file with your template content:

```jinja2
# {{ title }}

Author: {{ author }}
Date: {{ date }}

## Description

{{ description }}
```

### Template Variables

Use `{{ variable_name }}` for variable substitution:

```jinja2
class {{ name }}:
    """{{ description }}"""
    pass
```

### Conditionals

```jinja2
{% if author %}
Author: {{ author }}
{% endif %}
```

### Loops

```jinja2
{% for item in items %}
- {{ item }}
{% endfor %}
```

### Filters

```jinja2
{{ name | upper }}
{{ text | default('Default text') }}
{{ content | indent(4) }}
```

## Configuration File Format

Configuration files use YAML format:

```yaml
version: '1.0.0'

variables:
  author: "Your Name"
  email: "your.email@example.com"
  project_name: "my_project"
  description: "Project description"
  version: "1.0.0"

templates:
  my_template:
    file: "path/to/template.j2"
    description: "Template description"

output_dir: "./output"
```

## Examples

See the `examples/` directory for:

- `example_config.yaml` - Sample configuration file
- `generate_class.sh` - Script to generate a Python class
- `generate_readme.sh` - Script to generate a README

## Development

### Setup Development Environment

```bash
git clone https://github.com/InfinityXOneSystems/auto_templates.git
cd auto_templates
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black auto_templates tests
flake8 auto_templates tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

InfinityXOne Systems

## Support

For issues, questions, or contributions, please visit:
https://github.com/InfinityXOneSystems/auto_templates