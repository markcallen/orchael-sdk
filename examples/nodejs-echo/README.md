# Node.js Echo Agent for Orchael

A simple echo agent that demonstrates how to create a Node.js agent for Orchael.

## Overview

This example shows how to create a Node.js-based agent that can be uploaded to the Orchael backend. The agent implements a simple echo functionality that returns whatever input it receives.

## Project Structure

```
nodejs-echo/
├── config.yaml                    # Agent configuration
├── package.json                   # Node.js dependencies
└── nodejs_echo_processor/
    └── index.js                   # Main agent implementation
```

## Quick Start

### Install Dependencies

```bash
cd examples/nodejs-echo
npm install
```

### Run Locally

```bash
npm start
```

The agent will start on port 8000 (or the PORT environment variable).

### Test the Agent

```bash
# Test the chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, World!"}'

# Check health
curl http://localhost:8000/health

# Get history
curl http://localhost:8000/history
```

## Building for Orchael Deployment

### Using the SDK Build Command

```bash
# From the orchael-sdk directory
cd orchael-sdk
uv run orchael-sdk-cli build --config examples/nodejs-echo/config.yaml --output nodejs-echo-agent.zip
```

### Manual Build

You can also create the ZIP file manually:

```bash
cd examples/nodejs-echo
zip -r nodejs-echo-agent.zip . -x "node_modules/*" "*.log" ".git/*"
```

## Agent Configuration

The `config.yaml` file contains:

```yaml
processor_class: nodejs_echo_processor.NodejsEchoProcessor
agent_type: nodejs
runtime_version: 20.0.0
name: nodejs-echo-agent
version: 0.1.0
description: A simple echo agent for Orchael using Node.js
env:
  PORT: 8000
```

### Configuration Fields

- **processor_class**: The main class that implements the agent logic
- **agent_type**: Must be "nodejs" for Node.js agents
- **runtime_version**: Minimum Node.js version required (20.0.0 or higher)
- **name**: Agent name for identification
- **version**: Agent version
- **description**: Human-readable description
- **env**: Environment variables to set

## Implementation Details

### NodejsEchoProcessor Class

The main processor class implements:

- **processChat(chatInput)**: Processes incoming chat messages
- **getHistory()**: Returns chat history
- **constructor()**: Initializes the processor

### HTTP Endpoints

The agent exposes these endpoints:

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

## Dependencies

- **express**: Web framework for HTTP endpoints
- **cors**: Cross-origin resource sharing support
- **jest**: Testing framework (dev dependency)

## Requirements

- Node.js 20.0.0 or higher
- npm or yarn package manager

## Testing

```bash
npm test
```

## License

MIT License - see LICENSE file for details.
