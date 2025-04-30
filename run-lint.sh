#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run pylint on all Python files in the project
echo "Running pylint..."
pylint **/*.py

# Run flake8 for style guide enforcement
echo "Running flake8..."
flake8 .

# Run black to check code formatting
echo "Checking code formatting with black..."
black --check .

# Run isort to check import sorting
echo "Checking import sorting with isort..."
# Check if isort is installed
if ! command -v isort &> /dev/null
then
    echo "isort could not be found, please install it to check import sorting."
    exit 1
fi  
# Check import sorting  
isort . --check-only

# Run mypy for type checking
echo "Running mypy..."
mypy .

echo "Linting completed successfully!"