from typing import List, Optional, Union
from dataclasses import dataclass
from typing_extensions import TypedDict

class ChatHistoryEntry(TypedDict):
    """Represents a single entry in the chat history"""
    input: str
    output: str

class ChatInput(TypedDict):
    """Represents the input structure for the chat API"""
    input: str
    history: Optional[List[ChatHistoryEntry]]

class ChatOutput(TypedDict):
    """Represents the output structure from the chat API"""
    input: str
    output: str

class ChatError(TypedDict):
    """Represents an error response from the chat API"""
    error: str

# Union type for all possible response types
ChatResponse = Union[ChatOutput, ChatError]
