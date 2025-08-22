# Orchael SDK

A framework for building chat processors and chat applications in Python.

## Features

- **Chat Types**: Structured data types for chat inputs, outputs, and history
- **Processor Interface**: Abstract base class for implementing custom chat processors
- **Type Safety**: Full type hints and support for Python 3.10+
- **Extensible**: Easy to extend and customize for different use cases
- **CLI Tool**: Command-line interface for testing and using chat processors
- **Environment Configuration**: Automatic environment variable loading from config files

## Installation

### From Source

```bash
cd orchael-sdk
uv sync
```

## Quick Start

```python
from orchael_sdk import OrchaelChatProcessor, ChatInput, ChatOutput, ChatHistoryEntry
from typing import List

class MyChatProcessor(OrchaelChatProcessor):
    def __init__(self):
        self._history: List[ChatHistoryEntry] = []

    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        # Your custom logic here
        input_text = chat_input['input']
        output_text = f"Echo: {input_text}"

        # Update history
        history_entry: ChatHistoryEntry = {
            'input': input_text,
            'output': output_text
        }
        self._history.append(history_entry)

        return ChatOutput(
            input=input_text,
            output=output_text
        )

    def get_history(self) -> List[ChatHistoryEntry]:
        return self._history.copy()

# Usage
processor = MyChatProcessor()
result = processor.process_chat(ChatInput(
    input="Hello, world!",
    history=[]
))
print(result['output'])  # "Echo: Hello, world!"
```

## CLI Usage

The SDK includes a command-line interface for testing chat processors:

```bash
# Process a message
uv run python orchael_sdk_cli.py --input "Hello, world!" --config config.yaml

# Show chat history
uv run python orchael_sdk_cli.py --config config.yaml --history

# Get help
uv run python orchael_sdk_cli.py --help
```

### Configuration File

Create a `config.yaml` file to specify which processor to use:

```yaml
processor_class: my_module.MyChatProcessor
```

### Environment Variable Configuration

The SDK automatically loads environment variables from the `env` section of your config file:

```yaml
processor_class: my_module.MyChatProcessor
env:
  API_KEY: "your-api-key-here"
  MODEL_NAME: "gpt-4"
  TEMPERATURE: "0.7"
  DEBUG_MODE: "true"
```

These environment variables are automatically set before your processor is instantiated, making them available throughout your processor's lifecycle. You can access them using `os.getenv()` or `os.environ`.

**Example usage in a processor:**

```python
import os
from orchael_sdk import OrchaelChatProcessor

class MyProcessor(OrchaelChatProcessor):
    def __init__(self):
        # Environment variables are automatically available
        self.api_key = os.getenv('API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'default-model')
        self.temperature = float(os.getenv('TEMPERATURE', '0.5'))
```

See [CLI_README.md](CLI_README.md) for detailed CLI documentation.

## Core Components

### Chat Types

- `ChatInput`: Input structure with message and optional history
- `ChatOutput`: Output structure with processed input and response
- `ChatHistoryEntry`: Individual chat history entries
- `ChatError`: Error response structure
- `ChatResponse`: Union type for all possible responses

### OrchaelChatProcessor

Abstract base class that defines the interface for chat processors:

- `process_chat(chat_input: ChatInput) -> ChatOutput`: Process incoming chat
- `get_history() -> List[ChatHistoryEntry]`: Retrieve chat history

## Examples

The SDK includes several examples in the parent `examples/` directory:

- **`examples/echo/`**: Echo processor example with CLI demonstration
- **`examples/ollama/`**: Ollama integration example

## Development

### Setup

```bash
uv sync --dev
```

### Testing

```bash
uv run pytest
```

### Code Quality

```bash
uv run black .
uv run ruff check .
uv run mypy .
```

## Package Structure

```
orchael_sdk/
├── __init__.py               # Main package exports
├── chat_types.py             # Chat data structures
├── orchael_chat_processor.py # Abstract base class
└── py.typed                  # Type checking support
```

## Requirements

- Python 3.10 or higher
- typing-extensions (for TypedDict support)
- click (for CLI functionality)
- PyYAML (for configuration files)

## License

MIT License - see LICENSE file for details.
