#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate the virtual environment
source ./djangoenv/Scripts/activate

echo "Running Black to format code..."
black djangoapp/ djangoproj/ frontend/

echo "Running isort to sort imports..."
isort djangoapp/ djangoproj/ frontend/

echo "Running autoflake to remove unused imports..."
autoflake --remove-all-unused-imports --recursive --in-place djangoapp/ djangoproj/ frontend/

echo "Removing trailing whitespace from Python files..."
find . -type f -name "*.py" -exec sed -i 's/[ \t]*$//' {} +

echo "Running flake8 to check for remaining issues..."
flake8 djangoapp/ djangoproj/ frontend/

echo "All linting and formatting issues have been fixed successfully!"
