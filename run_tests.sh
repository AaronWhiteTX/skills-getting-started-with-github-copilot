#!/bin/bash
# Test runner script for FastAPI application

echo "Running FastAPI tests..."
echo "========================"

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing -v

echo ""
echo "Test run completed!"