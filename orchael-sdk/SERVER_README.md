# Orchael SDK FastAPI Server

This document describes how to use the FastAPI server that provides the same functionality as the CLI.

## Features

- **Health Check**: `/health` endpoint to verify server status
- **Chat Processing**: `/chat` endpoint to process chat inputs
- **Chat History**: `/chat/history` endpoint to retrieve chat history
- **Configuration**: Uses the same YAML configuration as the CLI

## Installation

The server dependencies are included in the main package. Install with:

```bash
uv install -e .
```

## Running the Server

### Using the CLI Script

```bash
# Run with default settings (port 8000, config.yaml)
orchael-sdk-server

# Run on a specific port
orchael-sdk-server --port 8080

# Run on a specific host and port
orchael-sdk-server --host 127.0.0.1 --port 9000

# Use a custom config file
orchael-sdk-server --config my_config.yaml
```

### Using Python Directly

```bash
# Run the server module directly
uv run python -m orchael_sdk.server

# Or import and run programmatically
python -c "
from orchael_sdk.server import run_server
run_server(host='0.0.0.0', port=8000, config_file='config.yaml')
"
```

## API Endpoints

### GET /health

Health check endpoint that returns server status.

**Response:**
```json
{
  "status": "ok"
}
```

### POST /chat

Process chat input and return response.

**Request Body:**
```json
{
  "input": "Hello, how are you?",
  "history": [
    {
      "input": "Previous message",
      "output": "Previous response"
    }
  ]
}
```

**Response:**
```json
{
  "input": "Hello, how are you?",
  "output": "I'm doing well, thank you for asking!"
}
```

### GET /chat/history

Retrieve chat history.

**Response:**
```json
{
  "history": [
    {
      "input": "Hello",
      "output": "Hi there!"
    },
    {
      "input": "How are you?",
      "output": "I'm doing well!"
    }
  ]
}
```

## Configuration

The server uses the same YAML configuration file as the CLI. Create a `config.yaml` file:

```yaml
processor_class: "examples.echo.echo_processor.EchoChatProcessor"
env:
  API_KEY: "your-api-key"
  MODEL_NAME: "gpt-4"
```

## Example Usage

### Starting the Server

```bash
# Start server
orchael-sdk-server --port 8000

# Server will be available at http://localhost:8000
```

### Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Process chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, world!", "history": []}'

# Get chat history
curl http://localhost:8000/chat/history
```

### Testing with Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())  # {"status": "ok"}

# Process chat
chat_data = {
    "input": "Hello, how are you?",
    "history": []
}
response = requests.post("http://localhost:8000/chat", json=chat_data)
print(response.json())  # {"input": "...", "output": "..."}

# Get history
response = requests.get("http://localhost:8000/chat/history")
print(response.json())  # {"history": [...]}
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

The server returns appropriate HTTP status codes:

- `200`: Success
- `500`: Internal server error (e.g., processor creation failed, chat processing error)

Error responses include a detail message:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run server tests only
uv run pytest tests/test_server.py

# Run with coverage
uv run pytest --cov=orchael_sdk tests/test_server.py
```

### Code Quality

```bash
# Format code
uv run black orchael_sdk/server.py

# Lint code
uv run ruff check orchael_sdk/server.py

# Type check
uv run mypy orchael_sdk/server.py
```

## Troubleshooting

### Common Issues

1. **Config file not found**: Ensure `config.yaml` exists in the current directory
2. **Processor class not found**: Check that the `processor_class` path in config is correct
3. **Port already in use**: Use a different port with `--port` option
4. **Import errors**: Ensure all dependencies are installed with `uv install -e .`

### Debug Mode

For debugging, you can run the server with more verbose output:

```bash
uv run python -m orchael_sdk.server
```

This will show detailed error messages and stack traces.
