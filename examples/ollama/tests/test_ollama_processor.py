"""
Tests for the OllamaChatProcessor example
"""

import os
import sys
import pytest

from pathlib import Path

# Add the current directory to the path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from ollama_processor import OllamaChatProcessor  # type: ignore[import-not-found]
    from orchael_sdk import ChatInput  # type: ignore[import-not-found]
except ImportError:
    # If orchael_sdk is not available, we'll skip these tests
    OllamaChatProcessor = None  # type: ignore[misc,assignment]
    ChatInput = None  # type: ignore[misc,assignment]


@pytest.mark.skipif(
    OllamaChatProcessor is None or ChatInput is None,
    reason="OllamaChatProcessor or ChatInput not available",
)
class TestOllamaProcessor:
    """Test the OllamaChatProcessor from examples"""

    def setup_method(self) -> None:
        """Set up test environment"""
        # Clear any existing test environment variables
        for key in ["OLLAMA_HOST", "OLLAMA_MODEL"]:
            if key in os.environ:
                del os.environ[key]

    def teardown_method(self) -> None:
        """Clean up test environment"""
        # Clean up test environment variables
        for key in ["OLLAMA_HOST", "OLLAMA_MODEL"]:
            if key in os.environ:
                del os.environ[key]

    def test_ollama_processor_default_config(self) -> None:
        """Test OllamaChatProcessor with default configuration"""
        processor = OllamaChatProcessor()

        # Test that the processor can be instantiated
        assert processor is not None
        assert hasattr(processor, "process_chat")
        assert hasattr(processor, "get_history")

    def test_ollama_processor_custom_host(self) -> None:
        """Test OllamaChatProcessor with custom host"""
        # Set custom environment variable
        os.environ["OLLAMA_HOST"] = "http://localhost:11434"

        processor = OllamaChatProcessor()

        # Test that the processor can be instantiated with custom host
        assert processor is not None

    def test_ollama_processor_custom_model(self) -> None:
        """Test OllamaChatProcessor with custom model"""
        # Set custom environment variable
        os.environ["OLLAMA_MODEL"] = "llama2:7b"

        processor = OllamaChatProcessor()

        # Test that the processor can be instantiated with custom model
        assert processor is not None

    def test_ollama_processor_interface_compliance(self) -> None:
        """Test that OllamaChatProcessor implements the required interface"""
        processor = OllamaChatProcessor()

        # Test that required methods exist
        assert hasattr(processor, "process_chat")
        assert hasattr(processor, "get_history")

        # Test that process_chat is callable
        assert callable(processor.process_chat)
        assert callable(processor.get_history)

    def test_ollama_processor_history_initialization(self) -> None:
        """Test that OllamaChatProcessor initializes with empty history"""
        processor = OllamaChatProcessor()

        # Test that history starts empty
        history = processor.get_history()
        assert isinstance(history, list)
        assert len(history) == 0
