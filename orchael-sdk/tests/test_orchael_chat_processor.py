"""
Tests for OrchaelChatProcessor abstract base class
"""

from abc import ABC
from typing import List, Set
from orchael_sdk.orchael_chat_processor import OrchaelChatProcessor
from orchael_sdk.chat_types import ChatInput, ChatOutput, ChatHistoryEntry


class ConcreteChatProcessor(OrchaelChatProcessor):
    """Concrete implementation for testing the abstract base class"""

    def __init__(self) -> None:
        self._history: List[ChatHistoryEntry] = []

    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        """Simple echo implementation for testing"""
        input_text = chat_input["input"]
        output_text = f"Echo: {input_text}"

        # Add to history
        self._history.append({"input": input_text, "output": output_text})

        return ChatOutput(input=input_text, output=output_text)

    def get_history(self) -> List[ChatHistoryEntry]:
        """Return chat history"""
        return self._history


class TestOrchaelChatProcessor:
    """Test OrchaelChatProcessor abstract base class"""

    def test_is_abstract_base_class(self) -> None:
        """Test that OrchaelChatProcessor is an abstract base class"""
        assert issubclass(OrchaelChatProcessor, ABC)

        # Verify it's abstract by checking if it has abstract methods
        abstract_methods: Set[str] = getattr(
            OrchaelChatProcessor, "__abstractmethods__", set()
        )
        assert len(abstract_methods) > 0

    def test_concrete_implementation_works(self) -> None:
        """Test that a concrete implementation works correctly"""
        processor = ConcreteChatProcessor()
        assert isinstance(processor, OrchaelChatProcessor)

        # Test process_chat method
        chat_input = ChatInput(input="Hello", history=None)
        result = processor.process_chat(chat_input)

        assert result["input"] == "Hello"
        assert result["output"] == "Echo: Hello"

        # Test get_history method
        history = processor.get_history()
        assert len(history) == 1
        assert history[0]["input"] == "Hello"
        assert history[0]["output"] == "Echo: Hello"

    def test_abstract_methods_exist(self) -> None:
        """Test that abstract methods are defined"""
        # Check that abstract methods exist
        assert hasattr(OrchaelChatProcessor, "process_chat")
        assert hasattr(OrchaelChatProcessor, "get_history")

    def test_method_signatures(self) -> None:
        """Test method signatures match expected types"""
        # Check process_chat signature
        process_chat_sig = OrchaelChatProcessor.process_chat.__annotations__
        assert process_chat_sig["chat_input"] == ChatInput
        assert process_chat_sig["return"] == ChatOutput

        # Check get_history signature
        get_history_sig = OrchaelChatProcessor.get_history.__annotations__
        assert get_history_sig["return"] == List[ChatHistoryEntry]
