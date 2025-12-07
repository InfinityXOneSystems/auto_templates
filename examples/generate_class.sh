#!/bin/bash
# Example: Generate a Python class using auto-templates

auto-templates generate python/class.py.j2 output/my_class.py \
  -v name=DataProcessor \
  -v description="A class for processing data" \
  -v class_description="Handles data processing operations" \
  -v author="John Doe"

echo "Generated: output/my_class.py"
