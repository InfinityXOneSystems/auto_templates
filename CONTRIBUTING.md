# Contributing to Auto Templates

Thank you for your interest in contributing to Auto Templates! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- pip (Python package installer)

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/auto_templates.git
   cd auto_templates
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the package in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards (see below)

3. Run tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

4. Run linters and formatters:
   ```bash
   black auto_templates tests
   flake8 auto_templates tests --max-line-length=100
   ```

### Coding Standards

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all public functions, classes, and methods
- Keep functions small and focused on a single responsibility
- Maximum line length: 100 characters

### Adding Templates

To add a new template:

1. Create your template file in the appropriate subdirectory of `auto_templates/templates/`
2. Use Jinja2 syntax for template variables
3. Add documentation in the README about the new template
4. Consider adding an example in the `examples/` directory

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=auto_templates --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_engine.py
```

### Writing Tests

- Write unit tests for all new functionality
- Place tests in the `tests/` directory
- Use descriptive test names that explain what is being tested
- Follow the existing test structure and conventions
- Aim for high code coverage (>80%)

## Submitting Changes

### Pull Request Process

1. Update the README.md if needed with details of changes
2. Update documentation for any new features or changes
3. Ensure all tests pass and code is properly formatted
4. Commit your changes with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: description of what was added"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference to any related issues
   - Screenshots for UI changes (if applicable)

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Examples:
```
Add template for Docker Compose files

- Create docker-compose.yml.j2 template
- Add example configuration
- Update README with usage instructions

Fixes #123
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose. Reviewers will check:

- Code quality and style
- Test coverage
- Documentation completeness
- Adherence to project conventions

## Reporting Bugs

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or logs (if applicable)

Use the GitHub issue tracker to report bugs.

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain why it would be useful to most users
- Consider whether it fits the project's scope and goals

## Questions and Support

- Check the README for documentation
- Look through existing issues and pull requests
- Create a new issue with the "question" label

## License

By contributing to Auto Templates, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the project README and release notes.

Thank you for contributing to Auto Templates! 🎉
