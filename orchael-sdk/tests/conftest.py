"""
Pytest configuration and shared fixtures
"""

import os
import tempfile
import pytest
from typing import Dict, Any, Generator


@pytest.fixture
def temp_config_file() -> Generator[str, None, None]:
    """Create a temporary config file for testing"""
    config_data = {
        "processor_class": "test_module.TestProcessor",
        "env": {"TEST_KEY": "test_value", "API_KEY": "test-api-key"},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        import yaml  # type: ignore[import-untyped]

        yaml.dump(config_data, f)
        config_file = f.name

    yield config_file

    # Clean up
    try:
        os.unlink(config_file)
    except OSError:
        pass


@pytest.fixture
def sample_chat_input() -> Dict[str, Any]:
    """Sample chat input for testing"""
    return {"input": "Hello, how are you?", "history": None}


@pytest.fixture
def sample_chat_history() -> list[Dict[str, str]]:
    """Sample chat history for testing"""
    return [
        {"input": "Hi there", "output": "Hello!"},
        {"input": "How are you?", "output": "I'm doing well, thanks!"},
    ]


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables before and after tests"""
    # Store original environment variables
    original_env = {}
    test_keys = [
        "TEST_KEY",
        "API_KEY",
        "ECHO_PREFIX",
        "ECHO_UPPERCASE",
        "ECHO_REPEAT_COUNT",
    ]

    for key in test_keys:
        if key in os.environ:
            original_env[key] = os.environ[key]
            del os.environ[key]

    yield

    # Restore original environment variables
    for key in test_keys:
        if key in original_env:
            os.environ[key] = original_env[key]
        elif key in os.environ:
            del os.environ[key]


@pytest.fixture(scope="session")
def examples_path() -> str:
    """Path to examples directory"""
    return os.path.join(os.path.dirname(__file__), "..", "examples")
