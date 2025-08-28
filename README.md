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

### Develop a new agent

```bash
python3 -m venv .venv
pip install "git+https://github.com/markcallen/orchael-sdk.git#egg=orchael-sdk&subdirectory=orchael-sdk" && pip freeze > requirements.txt
```

Create a module

```bash
mkdir echo_chat_processor
cd echo_chat_processor
```

Add a module file `__init__.py`

```python
# Echo processor package
from .echo_chat_processor import EchoChatProcessor

__all__ = ["EchoChatProcessor"]
```

Create a class the implements OrchaelChatProcessor

```python
from typing import List
from orchael_sdk import OrchaelChatProcessor, ChatInput, ChatOutput, ChatHistoryEntry


class EchoChatProcessor(OrchaelChatProcessor):
    """Simple echo processor that repeats input and demonstrates environment variable usage"""

    def __init__(self) -> None:
        pass

    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        input_text = chat_input["input"]

        # Apply transformations based on environment variables
        output_text = input_text

        # Create output
        output = ChatOutput(input=input_text, output=output_text)

        return output

    def get_history(self) -> List[ChatHistoryEntry]:
        pass

```

Register this in the `config.yaml` in the root directory

```yaml
processor_class: EchoChatProcessor
```

Now run using the `orchael-sdk-cli`

```bash
uv run orchael-sdk-cli chat --config config.yaml --input "hellow"
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
