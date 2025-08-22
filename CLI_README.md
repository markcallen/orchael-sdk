# Orchael SDK CLI

The Orchael SDK includes a command-line interface (CLI) for testing and using chat processors.

## Installation

The CLI is automatically installed when you install the orchael-sdk package:

```bash
uv pip install -e .
```

## Usage

### Basic Usage

```bash
# Process a single message
uv run python orchael_sdk_cli.py --input "Hello, world!" --config config.yaml

# Show chat history
uv run python orchael_sdk_cli.py --config config.yaml --history

# Use custom config file
uv run python orchael_sdk_cli.py --input "Test message" --config /path/to/config.yaml
```

### Configuration File

The CLI requires a YAML configuration file that specifies which processor class to use:

```yaml
processor_class: example3.example_processor.ExampleChatProcessor
```

The `processor_class` should be a string in the format `module.ClassName` that can be imported.

### Options

- `--config, -c`: Path to YAML configuration file (default: config.yaml)
- `--input, -i`: Input text to process (required unless --history is used)
- `--history`: Show chat history instead of processing input
- `--help`: Show help message

## Examples

### Example 1: Basic Chat Processing

```bash
# Create a config.yaml file
echo "processor_class: examples.echo.echo_processor.EchoChatProcessor" > config.yaml

# Process a message
uv run python orchael_sdk_cli.py --input "Hello from CLI!" --config config.yaml
# Output: Echo: Hello from CLI!
```

### Example 2: Viewing History

```bash
# After processing some messages, view history
uv run python orchael_sdk_cli.py --config config.yaml --history
```

### Example 3: Using with Custom Processors

```bash
# Create a config for your custom processor
echo "processor_class: my_module.MyCustomProcessor" > my_config.yaml

# Use the CLI with your processor
uv run python orchael_sdk_cli.py --input "Test" --config my_config.yaml
```

### Example 4: Using the Echo Example

```bash
# Use the built-in echo example
uv run python orchael_sdk_cli.py --input "Test message" --config examples/echo/config.yaml

# Run the echo demo
uv run python examples/echo/demo_cli.py
```

## Requirements

- Python 3.10+
- orchael-sdk package
- PyYAML
- Click

## Notes

- Each CLI run creates a new processor instance, so history is not preserved between runs
- The processor class must inherit from `OrchaelChatProcessor`
- The processor class must be importable from the current Python path
