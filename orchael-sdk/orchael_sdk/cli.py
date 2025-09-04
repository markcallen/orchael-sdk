#!/usr/bin/env python3
"""
CLI for Orchael SDK
"""

import importlib
import os
import sys
import zipfile
import tempfile
import shutil
from typing import Type, Dict, Any, cast

import click

try:
    import yaml
except ImportError:
    click.echo("Error: PyYAML is required. Install with: pip install PyYAML", err=True)
    sys.exit(1)

from .orchael_chat_processor import OrchaelChatProcessor
from .chat_types import ChatInput


def load_processor_class(
    class_path: str, config_file: str
) -> Type[OrchaelChatProcessor]:
    """Dynamically load a processor class from a string path like 'module.ClassName'"""
    try:
        # Add the config file's directory to Python path to enable relative imports
        config_dir = os.path.dirname(os.path.abspath(config_file))
        if config_dir not in sys.path:
            sys.path.insert(0, config_dir)

        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        processor_class = getattr(module, class_name)

        # Check if the attribute is actually a class
        if not isinstance(processor_class, type):
            raise AttributeError(f"'{class_name}' is not a class")

        if not issubclass(processor_class, OrchaelChatProcessor):
            raise ValueError(
                f"Class {class_path} does not inherit from OrchaelChatProcessor"
            )

        return processor_class
    except (ImportError, AttributeError, ValueError) as e:
        click.echo(f"Error loading processor class {class_path}: {e}", err=True)
        sys.exit(1)


def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        if not config or "processor_class" not in config:
            raise ValueError("Config file must contain 'processor_class' field")

        return cast(Dict[str, Any], config)
    except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
        click.echo(f"Error loading config file {config_file}: {e}", err=True)
        sys.exit(1)


def set_env_vars_from_config(config: Dict[str, Any]) -> None:
    """Set environment variables from the 'env' section of config"""
    if "env" in config and isinstance(config["env"], dict):
        for key, value in config["env"].items():
            if isinstance(value, (str, int, float, bool)):
                # Convert value to string and set as environment variable
                os.environ[key] = str(value)
                click.echo(f"Set environment variable: {key}={value}", err=True)


def validate_config_for_build(config: Dict[str, Any], config_file: str) -> None:
    """Validate configuration for building an agent package"""
    # Check required fields
    required_fields = ["processor_class", "agent_type", "runtime_version"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"config.yaml must contain '{field}' field")

    # Validate agent type
    agent_type = config["agent_type"]
    if agent_type not in ["python", "nodejs"]:
        raise ValueError("agent_type must be 'python' or 'nodejs'")

    # Validate runtime version
    runtime_version = str(config["runtime_version"])
    if agent_type == "python":
        if not _validate_python_version(runtime_version):
            raise ValueError(
                f"Invalid Python version: {runtime_version}. Must be 3.10 or higher"
            )
    elif agent_type == "nodejs":
        if not _validate_nodejs_version(runtime_version):
            raise ValueError(
                f"Invalid Node.js version: {runtime_version}. Must be 20 or higher"
            )

    # Test loading the processor class (only for Python agents)
    if agent_type == "python":
        try:
            processor_class = load_processor_class(
                config["processor_class"], config_file
            )
            # Try to instantiate the class
            processor_class()
            click.echo(
                f"✓ Successfully loaded processor class: {config['processor_class']}"
            )
        except Exception as e:
            raise ValueError(
                f"Failed to load processor class {config['processor_class']}: {e}"
            )
    elif agent_type == "nodejs":
        # For Node.js agents, just validate the file structure
        click.echo(f"✓ Node.js agent processor class: {config['processor_class']}")


def _validate_python_version(version: str) -> bool:
    """Validate Python version format and minimum version."""
    try:
        parts = version.split(".")
        if len(parts) < 2:
            return False

        major = int(parts[0])
        minor = int(parts[1])

        # Check minimum version (3.10)
        if major < 3:
            return False
        if major == 3 and minor < 10:
            return False

        return True
    except (ValueError, IndexError):
        return False


def _validate_nodejs_version(version: str) -> bool:
    """Validate Node.js version format and minimum version."""
    try:
        parts = version.split(".")
        if len(parts) < 1:
            return False

        major = int(parts[0])

        # Check minimum version (20)
        if major < 20:
            return False

        return True
    except (ValueError, IndexError):
        return False


def _copy_tree_excluding_cache(src: str, dst: str) -> None:
    """Copy a directory tree excluding __pycache__ directories and Python cache files"""
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            # Skip __pycache__ directories
            if item == "__pycache__":
                continue
            # Recursively copy other directories
            _copy_tree_excluding_cache(s, d)
        else:
            # Skip Python cache files
            if item.endswith((".pyc", ".pyo", ".pyd")):
                continue
            # Copy regular files
            shutil.copy2(s, d)


def create_agent_package(
    config_file: str, output_file: str, include_dependencies: bool = True
) -> None:
    """Create a ZIP package for uploading to the backend"""
    try:
        # Check if output file already exists and warn user
        if os.path.exists(output_file):
            click.echo(
                f"⚠️  Warning: Output file '{output_file}' already exists and will be overwritten.",
                err=True,
            )
            click.echo("   Press Ctrl+C to cancel or any key to continue...", err=True)
            try:
                input()
            except KeyboardInterrupt:
                click.echo("\nBuild cancelled.", err=True)
                sys.exit(0)

        # Load and validate config
        config = load_config(config_file)
        validate_config_for_build(config, config_file)

        config_dir = os.path.dirname(os.path.abspath(config_file))

        # Create temporary directory for packaging
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy config.yaml to temp directory
            shutil.copy2(config_file, os.path.join(temp_dir, "config.yaml"))

            # Copy processor module files
            processor_class = config["processor_class"]
            if "." in processor_class:
                module_path = processor_class.rsplit(".", 1)[0]
                module_dir = module_path.replace(".", "/")

                # Copy the entire module directory
                source_module_dir = os.path.join(config_dir, module_dir)
                if os.path.exists(source_module_dir):
                    dest_module_dir = os.path.join(temp_dir, module_dir)
                    # Use custom copy function to exclude __pycache__ directories
                    _copy_tree_excluding_cache(source_module_dir, dest_module_dir)
                else:
                    # Try to find the module file
                    module_file = f"{source_module_dir}.py"
                    if os.path.exists(module_file):
                        dest_module_file = os.path.join(temp_dir, f"{module_dir}.py")
                        os.makedirs(os.path.dirname(dest_module_file), exist_ok=True)
                        shutil.copy2(module_file, dest_module_file)
                    else:
                        raise ValueError(
                            f"Could not find module directory or file: {source_module_dir}"
                        )
            else:
                # Simple class name, look for any .py files in the config directory
                for file in os.listdir(config_dir):
                    if file.endswith(".py") and not file.startswith("__"):
                        shutil.copy2(os.path.join(config_dir, file), temp_dir)

            # Copy dependencies if requested
            if include_dependencies:
                # Copy requirements.txt or pyproject.toml if they exist
                for dep_file in ["requirements.txt", "pyproject.toml", "package.json"]:
                    dep_path = os.path.join(config_dir, dep_file)
                    if os.path.exists(dep_path):
                        shutil.copy2(dep_path, temp_dir)

            # Create ZIP file
            with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    # Remove __pycache__ directories from dirs to avoid walking into them
                    dirs[:] = [d for d in dirs if d != "__pycache__"]

                    for file in files:
                        # Skip Python cache files
                        if file.endswith((".pyc", ".pyo", ".pyd")):
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)

            click.echo(f"✓ Successfully created agent package: {output_file}")
            click.echo(f"  Agent type: {config['agent_type']}")
            click.echo(f"  Runtime version: {config['runtime_version']}")
            click.echo(f"  Processor class: {config['processor_class']}")

    except Exception as e:
        click.echo(f"Error creating agent package: {e}", err=True)
        sys.exit(1)


@click.group()
def cli() -> None:
    """Orchael SDK CLI"""
    pass


@cli.command()
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    help="Path to YAML configuration file (default: config.yaml)",
)
@click.option(
    "--output",
    "-o",
    default="agent.zip",
    help="Output ZIP file name (default: agent.zip)",
)
@click.option(
    "--no-deps",
    is_flag=True,
    help="Exclude dependency files (requirements.txt, pyproject.toml, package.json)",
)
def build(config: str, output: str, no_deps: bool) -> None:
    """Build an agent package for uploading to the backend"""
    create_agent_package(config, output, include_dependencies=not no_deps)


@cli.command()
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    help="Path to YAML configuration file (default: config.yaml)",
)
@click.option(
    "--input", "-i", help="Input text to process (required unless --history is used)"
)
@click.option("--history", is_flag=True, help="Show chat history")
def chat(config: str, input: str, history: bool) -> None:
    """Process chat input or show history"""

    # Load configuration
    config_data = load_config(config)
    processor_class_path = config_data["processor_class"]

    # Set environment variables from config before loading processor
    set_env_vars_from_config(config_data)

    # Load processor class
    processor_class = load_processor_class(processor_class_path, config)

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


@cli.command()
@click.option(
    "--host", "-h", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
)
@click.option(
    "--port", "-p", default=8000, type=int, help="Port to bind to (default: 8000)"
)
@click.option(
    "--config",
    "-c",
    default="config.yaml",
    help="Path to YAML configuration file (default: config.yaml)",
)
def server(host: str, port: int, config: str) -> None:
    """Run the Orchael SDK FastAPI server"""

    # Check if config file exists
    if not os.path.exists(config):
        click.echo(f"Error: Config file {config} not found", err=True)
        click.echo(
            "Please create a config.yaml file with the 'processor_class' field",
            err=True,
        )
        return

    click.echo(f"Starting Orchael SDK server on {host}:{port}")
    click.echo(f"Using config file: {config}")
    click.echo("Press Ctrl+C to stop the server")

    try:
        from .server import run_server

        run_server(host=host, port=port, config_file=config)
    except KeyboardInterrupt:
        click.echo("\nServer stopped by user")
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)


def main() -> None:
    """Main entry point for backward compatibility"""
    cli()


if __name__ == "__main__":
    cli()
