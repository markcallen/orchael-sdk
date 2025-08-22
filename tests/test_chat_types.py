"""
Tests for chat_types module
"""

from orchael_sdk.chat_types import (
    ChatInput,
    ChatOutput,
    ChatHistoryEntry,
    ChatError,
    ChatResponse,
)


class TestChatHistoryEntry:
    """Test ChatHistoryEntry TypedDict"""

    def test_chat_history_entry_creation(self) -> None:
        """Test creating a ChatHistoryEntry"""
        entry = ChatHistoryEntry(input="Hello", output="Hi there!")
        assert entry["input"] == "Hello"
        assert entry["output"] == "Hi there!"

    def test_chat_history_entry_types(self) -> None:
        """Test ChatHistoryEntry type validation"""
        entry = ChatHistoryEntry(input="Test input", output="Test output")
        assert isinstance(entry["input"], str)
        assert isinstance(entry["output"], str)


class TestChatInput:
    """Test ChatInput TypedDict"""

    def test_chat_input_without_history(self) -> None:
        """Test creating ChatInput without history"""
        chat_input = ChatInput(input="Hello", history=None)
        assert chat_input["input"] == "Hello"
        assert chat_input["history"] is None

    def test_chat_input_with_history(self) -> None:
        """Test creating ChatInput with history"""
        history = [ChatHistoryEntry(input="Previous", output="Previous response")]
        chat_input = ChatInput(input="Hello", history=history)
        assert chat_input["input"] == "Hello"
        assert chat_input["history"] == history
        assert len(chat_input["history"]) == 1

    def test_chat_input_empty_history(self) -> None:
        """Test creating ChatInput with empty history"""
        chat_input = ChatInput(input="Hello", history=[])
        assert chat_input["input"] == "Hello"
        assert chat_input["history"] == []


class TestChatOutput:
    """Test ChatOutput TypedDict"""

    def test_chat_output_creation(self) -> None:
        """Test creating a ChatOutput"""
        output = ChatOutput(input="Hello", output="Hi there!")
        assert output["input"] == "Hello"
        assert output["output"] == "Hi there!"

    def test_chat_output_types(self) -> None:
        """Test ChatOutput type validation"""
        output = ChatOutput(input="Test input", output="Test output")
        assert isinstance(output["input"], str)
        assert isinstance(output["output"], str)


class TestChatError:
    """Test ChatError TypedDict"""

    def test_chat_error_creation(self) -> None:
        """Test creating a ChatError"""
        error = ChatError(error="Something went wrong")
        assert error["error"] == "Something went wrong"

    def test_chat_error_type(self) -> None:
        """Test ChatError type validation"""
        error = ChatError(error="Test error message")
        assert isinstance(error["error"], str)


class TestChatResponse:
    """Test ChatResponse Union type"""

    def test_chat_response_can_be_output(self) -> None:
        """Test that ChatResponse can be a ChatOutput"""
        response: ChatResponse = ChatOutput(input="Hello", output="Hi!")
        # Type check: response should be treated as ChatOutput here
        # Since we know this is a ChatOutput, we can safely access its keys
        # Cast to dict to avoid TypedDict key access issues
        response_dict = dict(response)
        assert "input" in response_dict
        assert "output" in response_dict
        assert response_dict["input"] == "Hello"
        assert response_dict["output"] == "Hi!"

    def test_chat_response_can_be_error(self) -> None:
        """Test that ChatResponse can be a ChatError"""
        response: ChatResponse = ChatError(error="Error occurred")
        # Type check: response should be treated as ChatError here
        # Since we know this is a ChatError, we can safely access its keys
        # Cast to dict to avoid TypedDict key access issues
        response_dict = dict(response)
        assert "error" in response_dict
        assert response_dict["error"] == "Error occurred"

    def test_chat_response_type_annotations(self) -> None:
        """Test that type annotations work correctly"""
        from typing import get_args

        # Verify the union type includes both ChatOutput and ChatError
        args = get_args(ChatResponse)
        assert ChatOutput in args
        assert ChatError in args
