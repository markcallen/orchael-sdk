"""
Tests for the EchoChatProcessor example
"""

import os
import sys
import pytest

from pathlib import Path

# Add the echo_processor directory to the path
echo_dir = Path(__file__).parent.parent / "echo_processor"
sys.path.insert(0, str(echo_dir))

try:
    from echo_chat_processor import EchoChatProcessor
    from orchael_sdk import ChatInput
except ImportError:
    # If orchael_sdk is not available, we'll skip these tests
    EchoChatProcessor = None
    ChatInput = None


@pytest.mark.skipif(
    EchoChatProcessor is None or ChatInput is None,
    reason="EchoChatProcessor or ChatInput not available",
)
class TestEchoProcessor:
    """Test the EchoChatProcessor from examples"""

    def setup_method(self) -> None:
        """Set up test environment"""
        # Clear any existing test environment variables
        for key in ["ECHO_PREFIX", "ECHO_UPPERCASE", "ECHO_REPEAT_COUNT"]:
            if key in os.environ:
                del os.environ[key]

    def teardown_method(self) -> None:
        """Clean up test environment"""
        # Clean up test environment variables
        for key in ["ECHO_PREFIX", "ECHO_UPPERCASE", "ECHO_REPEAT_COUNT"]:
            if key in os.environ:
                del os.environ[key]

    def test_echo_processor_default_config(self) -> None:
        """Test EchoChatProcessor with default configuration"""
        processor = EchoChatProcessor()

        # Test default behavior
        chat_input = ChatInput(input="Hello World", history=None)
        result = processor.process_chat(chat_input)

        assert result["input"] == "Hello World"
        assert result["output"] == "Echo: Hello World"

        # Test history
        history = processor.get_history()
        assert len(history) == 1
        assert history[0]["input"] == "Hello World"
        assert history[0]["output"] == "Echo: Hello World"

    def test_echo_processor_custom_prefix(self) -> None:
        """Test EchoChatProcessor with custom prefix"""
        # Set custom environment variable
        os.environ["ECHO_PREFIX"] = "Custom: "

        processor = EchoChatProcessor()

        chat_input = ChatInput(input="Test", history=None)
        result = processor.process_chat(chat_input)

        assert result["output"] == "Custom: Test"

    def test_echo_processor_uppercase(self) -> None:
        """Test EchoChatProcessor with uppercase enabled"""
        # Set uppercase environment variable
        os.environ["ECHO_UPPERCASE"] = "true"

        processor = EchoChatProcessor()

        chat_input = ChatInput(input="hello world", history=None)
        result = processor.process_chat(chat_input)

        assert result["output"] == "Echo: HELLO WORLD"

    def test_echo_processor_repeat_count(self) -> None:
        """Test EchoChatProcessor with repeat count"""
        # Set repeat count environment variable
        os.environ["ECHO_REPEAT_COUNT"] = "3"

        processor = EchoChatProcessor()

        chat_input = ChatInput(input="test", history=None)
        result = processor.process_chat(chat_input)

        assert result["output"] == "Echo: test test test "

    def test_echo_processor_with_history(self) -> None:
        """Test EchoChatProcessor with existing history"""
        processor = EchoChatProcessor()

        # Add some history first
        chat_input1 = ChatInput(input="First message", history=None)
        processor.process_chat(chat_input1)

        # Process second message
        chat_input2 = ChatInput(input="Second message", history=processor.get_history())
        result = processor.process_chat(chat_input2)

        assert result["input"] == "Second message"
        assert result["output"] == "Echo: Second message"

        # Check total history
        history = processor.get_history()
        assert len(history) == 2
        assert history[0]["input"] == "First message"
        assert history[1]["input"] == "Second message"
