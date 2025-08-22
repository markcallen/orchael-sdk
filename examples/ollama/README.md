# Ollama Chat Processor Example

This example demonstrates how to use the Orchael SDK with Ollama, including the new environment variable configuration feature.

## Features

- **Environment Variable Configuration**: Automatically loads environment variables from `config.yaml`
- **Ollama Integration**: Uses LangChain to interact with Ollama models
- **Chat History**: Maintains conversation history
- **Configurable Parameters**: Model, URL, and temperature can be set via config

## Configuration

The `config.yaml` file contains both the processor class and environment variables:

```yaml
processor_class: ollama_processor.OllamaChatProcessor
env:
  OLLAMA_URL: "http://localhost:11434"
  OLLAMA_MODEL: "qwen3:0.6b"
  OLLAMA_TEMPERATURE: "0.7"
```

## Environment Variables

The following environment variables are automatically set from the config:

- `OLLAMA_URL`: The URL where Ollama is running (default: http://localhost:11434)
- `OLLAMA_MODEL`: The model name to use (default: llama2)
- `OLLAMA_TEMPERATURE`: The temperature setting for responses (default: 0.7)

## Usage

### Using the CLI

```bash
# Process a chat input
python -m orchael_sdk.cli --config config.yaml --input "What is machine learning?"

# Show chat history
python -m orchael_sdk.cli --config config.yaml --history
```

### Using the SDK directly

```python
from orchael_sdk import set_env_vars_from_config
import yaml

# Load config and set environment variables
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

set_env_vars_from_config(config)

# Now environment variables are available
import os
print(os.getenv('OLLAMA_URL'))  # http://localhost:11434
```

### Testing Environment Variables

Run the test script to see environment variables being set:

```bash
cd examples/ollama
python test_env.py
```

## How It Works

1. **CLI Integration**: The CLI automatically calls `set_env_vars_from_config()` before creating the processor instance
2. **Environment Setup**: Environment variables are set from the `env` section of the config file
3. **Processor Initialization**: The processor reads these environment variables during initialization
4. **Runtime Access**: Environment variables are available throughout the processor's lifecycle

## Customization

You can add more environment variables to the `env` section of `config.yaml`:

```yaml
env:
  OLLAMA_URL: "http://localhost:11434"
  OLLAMA_MODEL: "qwen3:0.6b"
  OLLAMA_TEMPERATURE: "0.7"
  CUSTOM_SETTING: "value"
  API_KEY: "your-secret-key"
```

All values are automatically converted to strings and set as environment variables.
