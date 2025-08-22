"""
Orchael SDK - A framework for building chat processors
"""

from .orchael_chat_processor import OrchaelChatProcessor
from .chat_types import ChatInput, ChatOutput, ChatHistoryEntry

__all__ = [
    'OrchaelChatProcessor',
    'ChatInput', 
    'ChatOutput', 
    'ChatHistoryEntry',
    'set_env_vars_from_config'
]


def set_env_vars_from_config(config: dict) -> None:
    """
    Set environment variables from the 'env' section of a config dictionary.
    
    Args:
        config: Configuration dictionary that may contain an 'env' section
        
    Example:
        config = {
            'processor_class': 'my_processor.MyProcessor',
            'env': {
                'API_KEY': 'your-api-key',
                'MODEL_NAME': 'gpt-4',
                'TEMPERATURE': '0.7'
            }
        }
        set_env_vars_from_config(config)
    """
    import os
    
    if 'env' in config and isinstance(config['env'], dict):
        for key, value in config['env'].items():
            if isinstance(value, (str, int, float, bool)):
                # Convert value to string and set as environment variable
                os.environ[key] = str(value)
