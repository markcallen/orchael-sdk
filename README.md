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
uv sync
```

### Run Examples

```bash
# Echo example
cd examples/echo
uv sync
uv run orchael-sdk-cli --config config.yaml --input "Hello World"
```

```bash
# Ollama example
cd examples/ollama
uv sync
```

Edit the `config.yaml` and use your ollama server and model

```bash
uv run orchael-sdk-cli --config config.yaml --input "What is machine learning?"
```

### Develop new agent

```bash
uv init -p 3.12
```

## Documentation

- **SDK Documentation**: See `orchael-sdk/README.md` for detailed SDK usage
- **CLI Documentation**: See `orchael-sdk/CLI_README.md` for command-line interface usage
- **Examples**: See `examples/` directory for working implementations

## Development

### SDK Development

```bash
cd orchael-sdk
uv sync
```

Always check before commiting
```bash
uv run pytest
uv run black .
uv run ruff check .
```

### Example Development

Each example has its own dependencies and can be developed independently:

```bash
cd examples/your-example
uv sync
# Add your own tests and development setup
```

## Requirements

- Python 3.10 or higher
- `uv` package manager (recommended)

## License

MIT License - see LICENSE file for details.
