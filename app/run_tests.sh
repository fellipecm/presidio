#!/bin/bash

# Test runner script for Presidio PII Scanner
echo "Running Presidio PII Scanner Tests..."

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/Scripts/activate
else
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Set test environment variables
export AZURE_STORAGE_ACCOUNT_NAME=test
export AZURE_STORAGE_ACCOUNT_KEY=test
export STORAGE_CONTAINER_NAME=test

# Run unit tests
echo "Running unit tests..."
python -m pytest tests/test_pii_scanner.py -v

# Run integration tests
echo "Running integration tests..."
python -m pytest tests/test_integration.py -v

# Run all tests with coverage (if coverage is installed)
if python -c "import coverage" 2>/dev/null; then
    echo "Running tests with coverage..."
    python -m coverage run -m pytest tests/ -v
    python -m coverage report
    python -m coverage html
    echo "Coverage report generated in htmlcov/"
else
    echo "Coverage not installed. Run 'pip install coverage' for coverage reports."
fi

echo "Test run completed!"
