#!/usr/bin/env python3
"""
CLI for Orchael SDK
"""

import importlib
import os
import sys
from pathlib import Path
from typing import Type, Dict, Any, cast

import click

try:
    import yaml
except ImportError:
    click.echo("Error: PyYAML is required. Install with: pip install PyYAML", err=True)
    sys.exit(1)

from .orchael_chat_processor import OrchaelChatProcessor
from .chat_types import ChatInput, ChatOutput


def load_processor_class(class_path: str) -> Type[OrchaelChatProcessor]:
    """Dynamically load a processor class from a string path like 'module.ClassName'"""
    try:
        module_name, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        processor_class = getattr(module, class_name)
        
        if not issubclass(processor_class, OrchaelChatProcessor):
            raise ValueError(f"Class {class_path} does not inherit from OrchaelChatProcessor")
        
        return cast(Type[OrchaelChatProcessor], processor_class)
    except (ImportError, AttributeError, ValueError) as e:
        click.echo(f"Error loading processor class {class_path}: {e}", err=True)
        sys.exit(1)


def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        if not config or 'processor_class' not in config:
            raise ValueError("Config file must contain 'processor_class' field")
        
        return cast(Dict[str, Any], config)
    except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
        click.echo(f"Error loading config file {config_file}: {e}", err=True)
        sys.exit(1)


def set_env_vars_from_config(config: Dict[str, Any]) -> None:
    """Set environment variables from the 'env' section of config"""
    if 'env' in config and isinstance(config['env'], dict):
        for key, value in config['env'].items():
            if isinstance(value, (str, int, float, bool)):
                # Convert value to string and set as environment variable
                os.environ[key] = str(value)
                click.echo(f"Set environment variable: {key}={value}", err=True)


@click.command()
@click.option('--config', '-c', default='config.yaml', 
              help='Path to YAML configuration file (default: config.yaml)')
@click.option('--input', '-i', 
              help='Input text to process (required unless --history is used)')
@click.option('--history', is_flag=True, 
              help='Show chat history')
def main(config: str, input: str, history: bool) -> None:
    """Orchael SDK CLI"""
    
    # Load configuration
    config_data = load_config(config)
    processor_class_path = config_data['processor_class']
    
    # Set environment variables from config before loading processor
    set_env_vars_from_config(config_data)
    
    # Load processor class
    processor_class = load_processor_class(processor_class_path)
    
    # Create processor instance
    try:
        processor = processor_class()
    except Exception as e:
        click.echo(f"Error creating processor instance: {e}", err=True)
        sys.exit(1)
    
    # Show history if requested
    if history:
        history_entries = processor.get_history()
        click.echo("Chat History:")
        for i, entry in enumerate(history_entries):
            click.echo(f"{i+1}. Input: {entry['input']}")
            click.echo(f"   Output: {entry['output']}")
            click.echo()
        return
    
    # Check if input is provided
    if not input:
        click.echo("Error: --input is required unless --history is used", err=True)
        sys.exit(1)
    
    # Process chat input
    try:
        chat_input = ChatInput(input=input, history=None)
        result = processor.process_chat(chat_input)
        
        click.echo(f"Output: {result['output']}")
        
    except Exception as e:
        click.echo(f"Error processing chat: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
