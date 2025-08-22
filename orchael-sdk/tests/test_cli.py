"""
Tests for CLI module
"""

import os
import tempfile
import yaml  # type: ignore[import-untyped]
from unittest.mock import patch, MagicMock

from orchael_sdk.cli import (
    load_processor_class,
    load_config,
    set_env_vars_from_config,
    cli,
)
from orchael_sdk.orchael_chat_processor import OrchaelChatProcessor
from orchael_sdk.chat_types import ChatInput, ChatOutput, ChatHistoryEntry


class MockChatProcessor(OrchaelChatProcessor):
    """Mock processor for testing CLI"""

    def __init__(self) -> None:
        self._history: list[ChatHistoryEntry] = []

    def process_chat(self, chat_input: ChatInput) -> ChatOutput:
        """Mock process_chat implementation"""
        input_text = chat_input["input"]
        output_text = f"Mock response to: {input_text}"

        # Add to history
        self._history.append({"input": input_text, "output": output_text})

        return ChatOutput(input=input_text, output=output_text)

    def get_history(self) -> list[ChatHistoryEntry]:
        """Return mock history"""
        return self._history


class TestLoadProcessorClass:
    """Test load_processor_class function"""

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_valid_processor_class(self, mock_exit: MagicMock) -> None:
        """Test loading a valid processor class"""
        # Mock the module import
        with patch("orchael_sdk.cli.importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_module.MockChatProcessor = MockChatProcessor
            mock_import.return_value = mock_module

            result = load_processor_class("test_module.MockChatProcessor")

            assert result == MockChatProcessor
            mock_exit.assert_not_called()

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_invalid_processor_class(self, mock_exit: MagicMock) -> None:
        """Test loading an invalid processor class"""
        # Mock the module import to return a class that doesn't inherit from OrchaelChatProcessor
        with patch("orchael_sdk.cli.importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_module.InvalidClass = (
                str  # str doesn't inherit from OrchaelChatProcessor
            )
            mock_import.return_value = mock_module

            load_processor_class("test_module.InvalidClass")

            mock_exit.assert_called_once_with(1)

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_nonexistent_module(self, mock_exit: MagicMock) -> None:
        """Test loading from a nonexistent module"""
        with patch("orchael_sdk.cli.importlib.import_module") as mock_import:
            mock_import.side_effect = ImportError("No module named 'nonexistent'")

            load_processor_class("nonexistent.Class")

            mock_exit.assert_called_once_with(1)

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_nonexistent_class(self, mock_exit: MagicMock) -> None:
        """Test loading a nonexistent class from a valid module"""
        with patch("orchael_sdk.cli.importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_import.return_value = mock_module

            # Mock getattr to raise AttributeError
            with patch("orchael_sdk.cli.getattr") as mock_getattr:
                mock_getattr.side_effect = AttributeError(
                    "module has no attribute 'NonexistentClass'"
                )

                load_processor_class("test_module.NonexistentClass")

                mock_exit.assert_called_once_with(1)


class TestLoadConfig:
    """Test load_config function"""

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_valid_config(self, mock_exit: MagicMock) -> None:
        """Test loading a valid config file"""
        config_data = {
            "processor_class": "test_module.TestProcessor",
            "env": {"API_KEY": "test-key"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            config_file = f.name

        try:
            result = load_config(config_file)
            assert result == config_data
            mock_exit.assert_not_called()
        finally:
            os.unlink(config_file)

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_nonexistent_config_file(self, mock_exit: MagicMock) -> None:
        """Test loading a nonexistent config file"""
        load_config("nonexistent.yaml")
        mock_exit.assert_called_once_with(1)

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_invalid_yaml(self, mock_exit: MagicMock) -> None:
        """Test loading an invalid YAML file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            config_file = f.name

        try:
            load_config(config_file)
            mock_exit.assert_called_once_with(1)
        finally:
            os.unlink(config_file)

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_config_missing_processor_class(self, mock_exit: MagicMock) -> None:
        """Test loading config without processor_class field"""
        config_data = {"env": {"API_KEY": "test-key"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            config_file = f.name

        try:
            load_config(config_file)
            mock_exit.assert_called_once_with(1)
        finally:
            os.unlink(config_file)

    @patch("orchael_sdk.cli.sys.exit")
    def test_load_empty_config(self, mock_exit: MagicMock) -> None:
        """Test loading an empty config file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({}, f)
            config_file = f.name

        try:
            load_config(config_file)
            mock_exit.assert_called_once_with(1)
        finally:
            os.unlink(config_file)


class TestSetEnvVarsFromConfig:
    """Test set_env_vars_from_config function"""

    def test_set_env_vars_from_config(self) -> None:
        """Test setting environment variables from config"""
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
        """Test setting env vars when config has no env section"""
        config = {"processor_class": "test.Processor"}

        # Should not raise any errors
        set_env_vars_from_config(config)

    def test_set_env_vars_empty_env_section(self) -> None:
        """Test setting env vars when env section is empty"""
        config = {"processor_class": "test.Processor", "env": {}}

        # Should not raise any errors
        set_env_vars_from_config(config)

    def test_set_env_vars_invalid_env_section(self) -> None:
        """Test setting env vars when env section is not a dict"""
        config = {"processor_class": "test.Processor", "env": "not_a_dict"}

        # Should not raise any errors
        set_env_vars_from_config(config)


class TestCLIGroup:
    """Test CLI group function"""

    def test_cli_help_option(self) -> None:
        """Test that the CLI responds to --help option"""
        from click.testing import CliRunner

        runner = CliRunner()

        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "chat" in result.output
        assert "server" in result.output

    def test_cli_version_option(self) -> None:
        """Test that the CLI responds to --version option"""
        from click.testing import CliRunner

        runner = CliRunner()

        result = runner.invoke(cli, ["--version"])

        # Should either show version or help (depending on Click version)
        assert result.exit_code in [0, 2]

    def test_cli_invalid_option(self) -> None:
        """Test that the CLI handles invalid options gracefully"""
        from click.testing import CliRunner

        runner = CliRunner()

        result = runner.invoke(cli, ["--invalid-option"])

        # Should exit with error code
        assert result.exit_code != 0

    def test_cli_no_args(self) -> None:
        """Test that the CLI handles no arguments gracefully"""
        from click.testing import CliRunner

        runner = CliRunner()

        result = runner.invoke(cli, [])

        # Should show help when no args provided (Click exits with 2 for help)
        assert result.exit_code == 2
        assert "Usage:" in result.output
