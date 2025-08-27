#!/usr/bin/env python3
"""
FastAPI server for Orchael SDK
"""

import importlib
import os
import sys
from typing import Type, Dict, Any, cast, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

try:
    import yaml
except ImportError:
    raise ImportError("PyYAML is required. Install with: pip install PyYAML")

from .orchael_chat_processor import OrchaelChatProcessor
from .chat_types import ChatInput, ChatHistoryEntry


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""

    input: str
    history: List[ChatHistoryEntry] = []


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    input: str
    output: str


class HealthResponse(BaseModel):
    """Response model for health endpoint"""

    status: str = "ok"


class ChatHistoryResponse(BaseModel):
    """Response model for chat history endpoint"""

    history: List[ChatHistoryEntry]


def load_processor_class(
    class_path: str, config_file: str
) -> Type[OrchaelChatProcessor]:
    """Dynamically load a processor class from a string path like 'module.ClassName'"""
    try:
        # Add the config file's directory to Python path to enable relative imports
        config_dir = os.path.dirname(os.path.abspath(config_file))
        if config_dir not in sys.path:
            sys.path.insert(0, config_dir)

        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        processor_class = getattr(module, class_name)

        # Check if the attribute is actually a class
        if not isinstance(processor_class, type):
            raise AttributeError(f"'{class_name}' is not a class")

        if not issubclass(processor_class, OrchaelChatProcessor):
            raise ValueError(
                f"Class {class_path} does not inherit from OrchaelChatProcessor"
            )

        return processor_class
    except (ImportError, AttributeError, ValueError) as e:
        raise ValueError(f"Error loading processor class {class_path}: {e}")


def load_config(config_file: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        # Use environment variable if set, otherwise use the default parameter
        config_path = os.getenv("ORCHAEL_CONFIG_FILE", config_file)

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        if not config or "processor_class" not in config:
            raise ValueError("Config file must contain 'processor_class' field")

        return cast(Dict[str, Any], config)
    except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
        raise ValueError(f"Error loading config file {config_path}: {e}")


def set_env_vars_from_config(config: Dict[str, Any]) -> None:
    """Set environment variables from the 'env' section of config"""
    if "env" in config and isinstance(config["env"], dict):
        for key, value in config["env"].items():
            if isinstance(value, (str, int, float, bool)):
                # Convert value to string and set as environment variable
                os.environ[key] = str(value)


# Global processor instance
processor: Optional[OrchaelChatProcessor] = None


def get_processor() -> OrchaelChatProcessor:
    """Get or create the processor instance"""
    global processor
    if processor is None:
        # Load configuration
        config_data = load_config()
        processor_class_path = config_data["processor_class"]

        # Set environment variables from config before loading processor
        set_env_vars_from_config(config_data)

        # Load processor class
        config_file = os.getenv("ORCHAEL_CONFIG_FILE", "config.yaml")
        processor_class = load_processor_class(processor_class_path, config_file)

        # Create processor instance
        try:
            processor = processor_class()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error creating processor instance: {e}"
            )

    return processor


# Create FastAPI app
app = FastAPI(
    title="Orchael SDK API",
    description="FastAPI server for Orchael SDK chat processing",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse()


@app.post("/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest) -> ChatResponse:
    """Process chat input and return response"""
    try:
        proc = get_processor()
        chat_input = ChatInput(input=request.input, history=request.history)
        result = proc.process_chat(chat_input)

        return ChatResponse(input=result["input"], output=result["output"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {e}")


@app.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history() -> ChatHistoryResponse:
    """Get chat history"""
    try:
        proc = get_processor()
        history = proc.get_history()
        return ChatHistoryResponse(history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chat history: {e}")


def run_server(
    host: str = "0.0.0.0", port: int = 8000, config_file: str = "config.yaml"
) -> None:
    """Run the FastAPI server"""
    # Set config file path for loading
    os.environ["ORCHAEL_CONFIG_FILE"] = config_file

    # Start the server
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
