# Orchael SDK Echo Example

This example demonstrates how to use the Orchael SDK to create a simple echo chat processor.

## Features

- `EchoChatProcessor`: A simple implementation that echoes back input with "Echo: " prefix
- Demonstrates basic SDK usage patterns
- Shows how to implement the `OrchaelChatProcessor` abstract base class
- Includes CLI integration example
- **NEW**: Includes comprehensive test suite

## Project Structure

```
examples/echo/
├── echo_processor/
│   └── echo_chat_processor.py
├── tests/
│   ├── __init__.py
│   └── test_echo_processor.py
├── config.yaml
├── pyproject.toml
├── README.md
└── uv.lock
```

## Installation

### From the examples directory
```bash
cd examples/echo
uv sync
```

## Usage

### CLI Usage

```bash
# From the project root directory
cd orchael-sdk
uv sync

# Go to the echo example directory and install dependencies
cd examples/echo
uv sync

# Run the echo processor using the CLI
uv run orchael-sdk-cli chat --config config.yaml --input "Hello World"

# Show chat history (note: each CLI call creates a new processor instance)
uv run orchael-sdk-cli chat --config config.yaml --history
```

## Testing

Run the test suite for this example:

```bash
cd examples/echo
uv sync --dev
uv run pytest
```

The tests cover:
- Default configuration behavior
- Custom prefix configuration
- Uppercase transformation
- Repeat count functionality
- History management

## Dependencies

- orchael-sdk (from parent directory)
- Python 3.10+

## Configuration

The `config.yaml` file specifies which processor class to use:

```yaml
processor_class: echo_processor.EchoChatProcessor
env:
  ECHO_PREFIX: "Echo (custom): "
  ECHO_UPPERCASE: "true"
  ECHO_REPEAT_COUNT: "2"
```

## Environment Variables

The echo processor supports several environment variables:

- `ECHO_PREFIX`: Custom prefix for echo responses (default: "Echo: ")
- `ECHO_UPPERCASE`: Convert input to uppercase if set to "true"
- `ECHO_REPEAT_COUNT`: Number of times to repeat the echo response

## What Changed

- **NEW**: Added comprehensive test suite in `tests/` directory
- **NEW**: Updated pyproject.toml with testing configuration
- **NEW**: Tests can be run independently from the main SDK
- Simplified directory structure
- Updated configuration to work with the new project structure
- Maintained the EchoChatProcessor functionality
- Updated import paths for cleaner usage
