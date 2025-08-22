# Orchael SDK Echo Example

This example demonstrates how to use the Orchael SDK to create a simple echo chat processor.

## Features

- `EchoChatProcessor`: A simple implementation that echoes back input with "Echo: " prefix
- Demonstrates basic SDK usage patterns
- Shows how to implement the `OrchaelChatProcessor` abstract base class
- Includes CLI integration example

## Usage

### CLI Usage

```bash
# From the root directory, build the orchael-sdk
uv build

# Go to the echo example directory
cd examples/echo

# Install dependencies
uv sync

# Run the echo processor using the CLI with uv
PYTHONPATH=. uv run orchael-sdk-cli --config config.yaml --input "Hello World"

# Or build and run with Python directly
uv build
pip install dist/orchael_sdk_echo_example-0.1.0-py3-none-any.whl
python -m orchael_sdk.cli --config config.yaml --input "Hello World"

# Show chat history (note: each CLI call creates a new processor instance)
python -m orchael_sdk.cli --config config.yaml --history
```

### Direct Usage

```python
from echo_processor import EchoChatProcessor
from orchael_sdk import ChatInput

# Create processor
processor = EchoChatProcessor()

# Process chat
result = processor.process_chat(ChatInput(
    input="Hello!",
    history=[]
))

print(result['output'])  # "Echo: Hello!"
```

## Dependencies

- orchael-sdk
- orchael-sdk-cli
- Python 3.10+

## Configuration

The `config.yaml` file specifies which processor class to use:

```yaml
processor_class: echo_processor.EchoChatProcessor
```

## What Changed

- Simplified directory structure by removing main.py and demo_cli.py
- Updated configuration to work directly with the orchael-sdk-cli
- Maintained the EchoChatProcessor functionality
- Updated import paths for cleaner usage
