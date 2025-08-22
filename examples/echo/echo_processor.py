"""
Simple echo implementation of OrchaelChatProcessor that demonstrates environment variable usage
"""

import os
from typing import List
from orchael_sdk import OrchaelChatProcessor, ChatInput, ChatOutput, ChatHistoryEntry


class EchoChatProcessor(OrchaelChatProcessor):
    """Simple echo processor that repeats input and demonstrates environment variable usage"""
    
    def __init__(self) -> None:
        self._history: List[ChatHistoryEntry] = []
        
        # Read configuration from environment variables
        self.prefix = os.getenv('ECHO_PREFIX', 'Echo: ')
        self.uppercase = os.getenv('ECHO_UPPERCASE', 'false').lower() == 'true'
        self.repeat_count = int(os.getenv('ECHO_REPEAT_COUNT', '1'))
        
        print(f"Echo processor initialized with:")
        print(f"  Prefix: '{self.prefix}'")
        print(f"  Uppercase: {self.uppercase}")
        print(f"  Repeat count: {self.repeat_count}")
    
    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        input_text = chat_input['input']
        
        # Apply transformations based on environment variables
        output_text = input_text
        if self.uppercase:
            output_text = output_text.upper()
        
        # Repeat the text if configured
        if self.repeat_count > 1:
            output_text = (output_text + ' ') * self.repeat_count
        
        # Add prefix
        output_text = self.prefix + output_text
        
        # Create output
        output = ChatOutput(
            input=input_text,
            output=output_text
        )
        
        # Add to history
        self._history.append({
            "input": input_text,
            "output": output_text
        })
        
        return output
    
    def get_history(self) -> List[ChatHistoryEntry]:
        """Return the chat history as an array of ChatHistoryEntry"""
        return self._history
