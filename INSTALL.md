# Installation Guide

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

## Installation Options

### 1. From Source (Development)

```bash
git clone <repository-url>
cd orchael-sdk
uv install -e .
```

### 2. From Built Package

```bash
# Install from the built wheel
uv pip install dist/orchael_sdk-0.1.0-py3-none-any.whl

# Or from the source distribution
uv pip install dist/orchael_sdk-0.1.0.tar.gz
```

### 3. Using pip

```bash
pip install .
```

## Building the Package

To build distributable packages:

```bash
# Install build tools
uv pip install build

# Build packages
uv run python -m build
```

This will create:
- `dist/orchael_sdk-0.1.0-py3-none-any.whl` - Wheel package
- `dist/orchael_sdk-0.1.0.tar.gz` - Source distribution

## Development Setup

```bash
# Install with development dependencies
uv install --dev

# Run tests
uv run pytest

# Code quality checks
uv run black .
uv run isort .
uv run ruff check .
uv run mypy .
```

## Examples

See the `example3/` directory for a working example of how to use the SDK.

## Package Structure

```
orchael_sdk/
├── __init__.py              # Main package exports
├── chat_types.py            # Chat data structures
├── orchael_chat_processor.py # Abstract base class
└── py.typed                 # Type checking support
```
