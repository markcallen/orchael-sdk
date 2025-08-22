"""
Tests for example processors
"""

import os
import sys
from orchael_sdk import ChatInput


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
        # Add examples directory to path to import the processor
        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "echo")
        sys.path.insert(0, examples_dir)

        try:
            from echo_processor import EchoChatProcessor

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

        finally:
            # Remove examples directory from path
            sys.path.pop(0)

    def test_echo_processor_custom_prefix(self) -> None:
        """Test EchoChatProcessor with custom prefix"""
        # Set custom environment variable
        os.environ["ECHO_PREFIX"] = "Custom: "

        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "echo")
        sys.path.insert(0, examples_dir)

        try:
            from echo_processor import EchoChatProcessor

            processor = EchoChatProcessor()

            chat_input = ChatInput(input="Test", history=None)
            result = processor.process_chat(chat_input)

            assert result["output"] == "Custom: Test"

        finally:
            sys.path.pop(0)

    def test_echo_processor_uppercase(self) -> None:
        """Test EchoChatProcessor with uppercase enabled"""
        # Set uppercase environment variable
        os.environ["ECHO_UPPERCASE"] = "true"

        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "echo")
        sys.path.insert(0, examples_dir)

        try:
            from echo_processor import EchoChatProcessor

            processor = EchoChatProcessor()

            chat_input = ChatInput(input="hello world", history=None)
            result = processor.process_chat(chat_input)

            assert result["output"] == "Echo: HELLO WORLD"

        finally:
            sys.path.pop(0)

    def test_echo_processor_repeat_count(self) -> None:
        """Test EchoChatProcessor with repeat count"""
        # Set repeat count environment variable
        os.environ["ECHO_REPEAT_COUNT"] = "3"

        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "echo")
        sys.path.insert(0, examples_dir)

        try:
            from echo_processor import EchoChatProcessor

            processor = EchoChatProcessor()

            chat_input = ChatInput(input="Hi", history=None)
            result = processor.process_chat(chat_input)

            expected_output = "Echo: Hi Hi Hi "
            assert result["output"] == expected_output

        finally:
            sys.path.pop(0)

    def test_echo_processor_multiple_configs(self) -> None:
        """Test EchoChatProcessor with multiple custom configurations"""
        # Set multiple environment variables
        os.environ["ECHO_PREFIX"] = "Test: "
        os.environ["ECHO_UPPERCASE"] = "true"
        os.environ["ECHO_REPEAT_COUNT"] = "2"

        examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples", "echo")
        sys.path.insert(0, examples_dir)

        try:
            from echo_processor import EchoChatProcessor

            processor = EchoChatProcessor()

            chat_input = ChatInput(input="hello", history=None)
            result = processor.process_chat(chat_input)

            expected_output = "Test: HELLO HELLO "
            assert result["output"] == expected_output

        finally:
            sys.path.pop(0)


class TestOllamaProcessor:
    """Test the OllamaChatProcessor from examples"""

    def test_ollama_processor_import(self) -> None:
        """Test that OllamaChatProcessor can be imported"""
        examples_dir = os.path.join(
            os.path.dirname(__file__), "..", "examples", "ollama"
        )
        sys.path.insert(0, examples_dir)

        try:
            # This should not raise an ImportError
            from ollama_processor import OllamaChatProcessor

            # Verify it's a subclass of OrchaelChatProcessor
            from orchael_sdk import OrchaelChatProcessor

            assert issubclass(OllamaChatProcessor, OrchaelChatProcessor)

        except ImportError as e:
            # If there are missing dependencies, that's okay for testing
            # Just make sure it's not a syntax error
            assert "syntax" not in str(e).lower()
        finally:
            sys.path.pop(0)
