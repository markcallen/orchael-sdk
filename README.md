# Orchael SDK

A framework for building chat processors and chat applications in Python.

## Project Structure

This repository contains:

- **`orchael-sdk/`** - The main SDK package with all core functionality
- **`examples/`** - Example implementations and usage demonstrations

## Quick Start

### Install the SDK

```bash
cd orchael-sdk
uv install
```

### Development Installation

```bash
cd orchael-sdk
uv install -e .
```

### Run Examples

```bash
# Echo example
cd examples/echo
uv install
uv run python -m echo_processor.echo_chat_processor

# Ollama example
cd examples/ollama
uv install
uv run python ollama_processor.py
```

## Documentation

- **SDK Documentation**: See `orchael-sdk/README.md` for detailed SDK usage
- **CLI Documentation**: See `orchael-sdk/CLI_README.md` for command-line interface usage
- **Examples**: See `examples/` directory for working implementations

## Development

### SDK Development

```bash
cd orchael-sdk
uv install --dev
uv run pytest
uv run black .
uv run ruff check .
uv run mypy .
```

### Example Development

Each example has its own dependencies and can be developed independently:

```bash
cd examples/your-example
uv install --dev
# Add your own tests and development setup
```

## Requirements

- Python 3.10 or higher
- `uv` package manager (recommended)

## License

MIT License - see LICENSE file for details.
