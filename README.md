# Orchael SDK

A framework for building chat processors and chat applications in Python and Node.js.

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
# Python Echo example
cd examples/echo
uv sync
uv run orchael-sdk-cli --config config.yaml --input "Hello World"
```

```bash
# Node.js Echo example
cd examples/nodejs-echo
npm install
npm start
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

## Creating Sample Agents

The Orchael SDK supports both Python and Node.js agents. Here's how to create sample agents for both platforms:

### Python Agent Example

#### 1. Create Project Structure

```bash
mkdir my-python-agent
cd my-python-agent
mkdir my_agent_processor
```

#### 2. Create Configuration

Create `config.yaml`:

```yaml
processor_class: my_agent_processor.MyAgentProcessor
agent_type: python
runtime_version: 3.10
name: my-python-agent
version: 0.1.0
description: A sample Python agent for Orchael
env:
  CUSTOM_VAR: "value"
```

#### 3. Implement the Agent

Create `my_agent_processor/__init__.py`:

```python
from .my_agent_processor import MyAgentProcessor

__all__ = ["MyAgentProcessor"]
```

Create `my_agent_processor/my_agent_processor.py`:

```python
from typing import List
from orchael_sdk import OrchaelChatProcessor, ChatInput, ChatOutput, ChatHistoryEntry


class MyAgentProcessor(OrchaelChatProcessor):
    """Sample Python agent processor"""

    def __init__(self) -> None:
        self.history = []

    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        input_text = chat_input["input"]

        # Your custom logic here
        output_text = f"Python Agent says: {input_text}"

        # Store in history
        self.history.append({
            "input": input_text,
            "output": output_text
        })

        return ChatOutput(input=input_text, output=output_text)

    def get_history(self) -> List[ChatHistoryEntry]:
        return self.history
```

#### 4. Create Dependencies

Create `pyproject.toml`:

```toml
[project]
name = "my-python-agent"
version = "0.1.0"
description = "A sample Python agent for Orchael"
requires-python = ">=3.10"
dependencies = [
    "orchael-sdk @ {root:uri}/../orchael-sdk"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["my_agent_processor"]
```

#### 5. Build and Test

```bash
# Install dependencies
uv sync

# Test locally
uv run orchael-sdk-cli chat --config config.yaml --input "Hello World"

# Build for deployment
uv run orchael-sdk-cli build --config config.yaml --output my-python-agent.zip
```

### Node.js Agent Example

#### 1. Create Project Structure

```bash
mkdir my-nodejs-agent
cd my-nodejs-agent
mkdir my_agent_processor
```

#### 2. Create Configuration

Create `config.yaml`:

```yaml
processor_class: my_agent_processor.MyAgentProcessor
agent_type: nodejs
runtime_version: 20.0.0
name: my-nodejs-agent
version: 0.1.0
description: A sample Node.js agent for Orchael
env:
  PORT: 8000
```

#### 3. Create Package Configuration

Create `package.json`:

```json
{
  "name": "my-nodejs-agent",
  "version": "0.1.0",
  "description": "A sample Node.js agent for Orchael",
  "main": "my_agent_processor/index.js",
  "scripts": {
    "start": "node my_agent_processor/index.js",
    "test": "jest"
  },
  "engines": {
    "node": ">=20.0.0"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  }
}
```

#### 4. Implement the Agent

Create `my_agent_processor/index.js`:

```javascript
const express = require('express');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());

class MyAgentProcessor {
    constructor() {
        this.history = [];
    }

    processChat(chatInput) {
        const input = chatInput.input;

        // Your custom logic here
        const output = `Node.js Agent says: ${input}`;

        // Store in history
        this.history.push({
            input: input,
            output: output,
            timestamp: new Date().toISOString()
        });

        return {
            input: input,
            output: output
        };
    }

    getHistory() {
        return this.history;
    }
}

const processor = new MyAgentProcessor();

// Chat endpoint
app.post('/chat', (req, res) => {
    try {
        const chatInput = req.body;

        if (!chatInput.input) {
            return res.status(400).json({
                error: 'Missing input field'
            });
        }

        const result = processor.processChat(chatInput);
        res.json(result);
    } catch (error) {
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// History endpoint
app.get('/history', (req, res) => {
    try {
        const history = processor.getHistory();
        res.json(history);
    } catch (error) {
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString()
    });
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Node.js Agent running on port ${port}`);
});

module.exports = { MyAgentProcessor };
```

#### 5. Build and Test

```bash
# Install dependencies
npm install

# Test locally
npm start

# In another terminal, test the agent
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello World"}'

# Build for deployment (using the SDK build command)
cd ../orchael-sdk
uv run orchael-sdk-cli build --config ../my-nodejs-agent/config.yaml --output my-nodejs-agent.zip
```

## Building Agents for Deployment

### Using the Build Command

The SDK provides a `build` command that validates your agent and creates a ZIP file ready for upload:

```bash
# Build a Python agent
uv run orchael-sdk-cli build --config config.yaml --output my-agent.zip

# Build a Node.js agent
uv run orchael-sdk-cli build --config config.yaml --output my-agent.zip

# Build without dependencies
uv run orchael-sdk-cli build --config config.yaml --output my-agent.zip --no-deps
```

### Build Validation

The build command validates:

- **Required fields**: `processor_class`, `agent_type`, `runtime_version`
- **Agent type**: Must be "python" or "nodejs"
- **Runtime version**:
  - Python: 3.10 or higher
  - Node.js: 20.0.0 or higher
- **Processor class**: Must be loadable and instantiable
- **File structure**: Ensures all necessary files are included

### Manual Build

You can also create ZIP files manually:

```bash
# Python agent
cd my-python-agent
zip -r my-agent.zip . -x "*.pyc" "__pycache__/*" ".git/*" ".venv/*"

# Node.js agent
cd my-nodejs-agent
zip -r my-agent.zip . -x "node_modules/*" "*.log" ".git/*"
```

## Configuration Requirements

### Required Fields

All agents must include these fields in `config.yaml`:

```yaml
processor_class: your_module.YourProcessorClass
agent_type: python  # or nodejs
runtime_version: 3.10  # or 20.0.0 for Node.js
```

### Optional Fields

```yaml
name: my-agent-name
version: 0.1.0
description: Human-readable description
env:
  CUSTOM_VAR: value
  ANOTHER_VAR: another_value
```

## Agent Protocol

### Python Agents

Python agents must inherit from `OrchaelChatProcessor` and implement:

```python
def process_chat(self, chat_input: ChatInput) -> ChatOutput:
    # Your logic here
    return ChatOutput(input=input_text, output=output_text)

def get_history(self) -> List[ChatHistoryEntry]:
    # Return chat history
    return self.history
```

### Node.js Agents

Node.js agents must expose HTTP endpoints:

- **POST /chat**: Process chat input
- **GET /history**: Get chat history
- **GET /health**: Health check

Request/response format:

```json
// Request
{
  "input": "User input",
  "history": [...],
  "sessionid": "optional"
}

// Response
{
  "input": "User input",
  "output": "Agent response"
}
```

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
uv sync  # for Python
npm install  # for Node.js
# Add your own tests and development setup
```

## Requirements

- Python 3.10 or higher (for Python agents)
- Node.js 20.0.0 or higher (for Node.js agents)
- `uv` package manager (recommended for Python)
- `npm` or `yarn` (for Node.js)

## License

MIT License - see LICENSE file for details.
