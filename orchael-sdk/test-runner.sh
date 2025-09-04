#!/bin/bash

# Orchael SDK Test Runner Script

echo "🧪 Orchael SDK Test Runner"
echo "=========================="

# Check if we're in the right directory
if [ ! -d "orchael_sdk" ]; then
    echo "❌ Error: Please run this script from the orchael-sdk root directory"
    exit 1
fi

# Check if pytest is available
if ! uv run python -c "import pytest" 2>/dev/null; then
    echo "❌ pytest is not installed. Installing dev dependencies..."
    if ! uv add --dev pytest pytest-cov mypy ruff; then
        echo "❌ Failed to install dev dependencies"
        exit 1
    fi
fi

echo "✅ pytest is available"

# Run tests
echo ""
echo "Running tests..."
echo "================"

# Run unit tests
echo "Running unit tests..."
if uv run pytest tests/ -v --tb=short; then
    echo "✅ Unit tests passed"
else
    echo "❌ Unit tests failed"
    exit 1
fi

# Run tests with coverage
echo ""
echo "Running tests with coverage..."
echo "=============================="
if uv run pytest tests/ --cov=orchael_sdk --cov-report=term-missing; then
    echo "✅ Coverage tests passed"
else
    echo "❌ Coverage tests failed"
    exit 1
fi

# Check if mypy is available
if uv run python -c "import mypy" 2>/dev/null; then
    echo ""
    echo "Running type checking..."
    echo "======================="
    if uv run mypy orchael_sdk/; then
        echo "✅ Type checking passed"
    else
        echo "❌ Type checking failed"
        exit 1
    fi
else
    echo "⚠️  mypy not available, skipping type checking"
fi

# Check if ruff is available
if uv run python -c "import ruff" 2>/dev/null; then
    echo ""
    echo "Running linting..."
    echo "=================="
    if uv run ruff check orchael_sdk/ tests/; then
        echo "✅ Linting passed"
    else
        echo "❌ Linting failed"
        exit 1
    fi
else
    echo "⚠️  ruff not available, skipping linting"
fi

echo ""
echo "🎉 All tests and checks completed successfully!"
