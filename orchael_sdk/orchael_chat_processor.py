"""
Base class for Orchael chat processors
"""

from abc import ABC, abstractmethod
from typing import List
from .chat_types import ChatInput, ChatOutput, ChatHistoryEntry


class OrchaelChatProcessor(ABC):
    """Base class for chat processors that implement the Orchael chat interface"""
    
    @abstractmethod
    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        """Process a chat input and return a chat output"""
        pass
    
    @abstractmethod
    def get_history(self) -> List[ChatHistoryEntry]:
        """Return the chat history as an array of ChatHistoryEntry"""
        pass
