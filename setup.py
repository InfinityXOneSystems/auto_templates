from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto_templates",
    version="1.0.0",
    author="InfinityXOne Systems",
    description="A comprehensive auto-templating system for generating files and projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/InfinityXOneSystems/auto_templates",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "jinja2>=3.0.0",
        "pyyaml>=5.4.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "auto-templates=auto_templates.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "auto_templates": ["templates/**/*"],
    },
)
