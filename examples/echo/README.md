# Orchael SDK Echo Example

This example demonstrates how to use the Orchael SDK to create a simple echo chat processor.

## Features

- `EchoChatProcessor`: A simple implementation that echoes back input with "Echo: " prefix
- Demonstrates basic SDK usage patterns
- Shows how to implement the `OrchaelChatProcessor` abstract base class
- Includes CLI integration example
- **NEW**: Includes comprehensive test suite
- **NEW**: Includes build and deployment instructions for Orchael

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

## Building for Orchael Deployment

### Using the SDK Build Command

```bash
# From the orchael-sdk directory
cd orchael-sdk
uv run orchael-sdk-cli build --config ../examples/echo/config.yaml --output echo-agent.zip
```

**Note**: If the output file already exists, the build command will warn you before overwriting it. You can press Ctrl+C to cancel or any key to continue.

### Manual Build

You can also create the ZIP file manually:

```bash
cd examples/echo
zip -r echo-agent.zip . -x "__pycache__/*" "*.pyc" "*.pyo" "*.pyd" ".git/*" "tests/*" "*.log"
```

## Agent Configuration

The `config.yaml` file contains:

```yaml
processor_class: echo_processor.EchoChatProcessor
agent_type: python
runtime_version: 3.10
name: echo-agent
version: 0.1.0
description: A simple echo agent for Orchael using Python
env:
  ECHO_PREFIX: "Echo: "
  ECHO_UPPERCASE: "false"
  ECHO_REPEAT_COUNT: "1"
```

### Configuration Fields

- **processor_class**: The main class that implements the agent logic
- **agent_type**: Must be "python" for Python agents
- **runtime_version**: Minimum Python version required (3.10 or higher)
- **name**: Agent name for identification
- **version**: Agent version
- **description**: Human-readable description
- **env**: Environment variables to set

## Implementation Details

### EchoChatProcessor Class

The main processor class implements:

- **process_chat(chat_input)**: Processes incoming chat messages
- **get_history()**: Returns chat history
- **__init__()**: Initializes the processor with configuration

### HTTP Endpoints

When deployed to Orchael, the agent exposes these endpoints:

- **POST /chat**: Process chat input
- **GET /history**: Get chat history
- **GET /health**: Health check

### Request Format

```json
{
  "input": "User input text",
  "history": [
    {"input": "Previous input", "output": "Previous output"}
  ],
  "sessionid": "optional-session-id"
}
```

### Response Format

```json
{
  "input": "User input text",
  "output": "Agent response text"
}
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

## Requirements

- Python 3.10 or higher
- uv package manager (recommended) or pip

## What Changed

- **NEW**: Added comprehensive test suite in `tests/` directory
- **NEW**: Updated pyproject.toml with testing configuration
- **NEW**: Tests can be run independently from the main SDK
- **NEW**: Added build and deployment instructions for Orchael
- **NEW**: Added agent configuration details
- **NEW**: Added HTTP endpoint documentation
- Simplified directory structure
- Updated configuration to work with the new project structure
- Maintained the EchoChatProcessor functionality
- Updated import paths for cleaner usage
