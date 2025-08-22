"""
Tests for main package functionality
"""

import os
from orchael_sdk import (
    set_env_vars_from_config,
    OrchaelChatProcessor,
    ChatInput,
    ChatOutput,
    ChatHistoryEntry,
)


class TestMainPackage:
    """Test main package functionality"""

    def test_set_env_vars_from_config(self) -> None:
        """Test set_env_vars_from_config function from main package"""
        config = {
            "processor_class": "test.Processor",
            "env": {
                "TEST_KEY": "test_value",
                "NUMBER": 42,
                "FLOAT": 3.14,
                "BOOLEAN": True,
            },
        }

        # Clear any existing test environment variables
        for key in ["TEST_KEY", "NUMBER", "FLOAT", "BOOLEAN"]:
            if key in os.environ:
                del os.environ[key]

        set_env_vars_from_config(config)

        assert os.environ["TEST_KEY"] == "test_value"
        assert os.environ["NUMBER"] == "42"
        assert os.environ["FLOAT"] == "3.14"
        assert os.environ["BOOLEAN"] == "True"

        # Clean up
        for key in ["TEST_KEY", "NUMBER", "FLOAT", "BOOLEAN"]:
            if key in os.environ:
                del os.environ[key]

    def test_set_env_vars_no_env_section(self) -> None:
        """Test set_env_vars_from_config when config has no env section"""
        config = {"processor_class": "test.Processor"}

        # Should not raise any errors
        set_env_vars_from_config(config)

    def test_set_env_vars_empty_env_section(self) -> None:
        """Test set_env_vars_from_config when env section is empty"""
        config = {"processor_class": "test.Processor", "env": {}}

        # Should not raise any errors
        set_env_vars_from_config(config)

    def test_set_env_vars_invalid_env_section(self) -> None:
        """Test set_env_vars_from_config when env section is not a dict"""
        config = {"processor_class": "test.Processor", "env": "not_a_dict"}

        # Should not raise any errors
        set_env_vars_from_config(config)

    def test_imports_work(self) -> None:
        """Test that all main package imports work correctly"""
        # Test that we can import the main classes
        assert OrchaelChatProcessor is not None
        assert ChatInput is not None
        assert ChatOutput is not None
        assert ChatHistoryEntry is not None
        assert set_env_vars_from_config is not None

    def test_package_all_contains_expected_items(self) -> None:
        """Test that __all__ contains the expected items"""
        from orchael_sdk import __all__

        expected_items = {
            "OrchaelChatProcessor",
            "ChatInput",
            "ChatOutput",
            "ChatHistoryEntry",
            "set_env_vars_from_config",
        }

        assert set(__all__) == expected_items
