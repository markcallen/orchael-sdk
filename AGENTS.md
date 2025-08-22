# AGENTS.md

## 📦 Project Overview

**Orchael-SDK** is a Python library providing access to the Orchael agent world

- **Repository:** [markcallen/orchael-sdk](https://github.com/markcallen/orchael-sdk)
- **Primary Language:** Python 3.10+
- **Test Framework:** `pytest`
- **Formatting** `black`
- **Linting:** `ruff`
- **Type Checking:** `mypy`
- **CI:** GitHub Actions (matrix for backends/OS with Dockerized services)
- **Issue Tracking:** GitHub Issues

## 🚦 Quick Start

1. **Prerequisites:**

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

2. Installation Options

2.1. From Source (Development)

```bash
git clone <repository-url>
cd orchael-sdk
uv install -e .
```

2.2 From Built Package

```bash
# Install from the built wheel
uv pip install dist/orchael_sdk-0.1.0-py3-none-any.whl

# Or from the source distribution
uv pip install dist/orchael_sdk-0.1.0.tar.gz
```

2.3 Using pip

```bash
pip install .
```

3 Building the Package

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

See the `examples/echo` directory for a working example of how to use the SDK.

## Package Structure

```
orchael_sdk/
├── __init__.py               # Main package exports
├── chat_types.py             # Chat data structures
├── orchael_chat_processor.py # Abstract base class
└── py.typed                  # Type checking support
```
