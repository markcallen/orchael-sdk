#!/usr/bin/env python3
"""
Test script to demonstrate environment variable loading from config.yaml
"""

import os
import yaml  # type: ignore
from orchael_sdk import set_env_vars_from_config

def main() -> None:
    print("Before loading config:")
    print(f"OLLAMA_URL: {os.getenv('OLLAMA_URL', 'Not set')}")
    print(f"OLLAMA_MODEL: {os.getenv('OLLAMA_MODEL', 'Not set')}")
    print(f"OLLAMA_TEMPERATURE: {os.getenv('OLLAMA_TEMPERATURE', 'Not set')}")
    print()
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Set environment variables
    set_env_vars_from_config(config)
    
    print("After loading config:")
    print(f"OLLAMA_URL: {os.getenv('OLLAMA_URL', 'Not set')}")
    print(f"OLLAMA_MODEL: {os.getenv('OLLAMA_MODEL', 'Not set')}")
    print(f"OLLAMA_TEMPERATURE: {os.getenv('OLLAMA_TEMPERATURE', 'Not set')}")

if __name__ == "__main__":
    main()
