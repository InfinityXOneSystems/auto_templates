#!/bin/bash
# Example: Generate a README using auto-templates with config file

auto-templates generate docs/README.md.j2 output/README.md \
  -c example_config.yaml

echo "Generated: output/README.md"
