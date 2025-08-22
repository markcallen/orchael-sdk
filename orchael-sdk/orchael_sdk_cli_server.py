#!/usr/bin/env python3
"""
CLI script to run the Orchael SDK FastAPI server
"""

import click
import os
from orchael_sdk.server import run_server


@click.command()
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
def main(host: str, port: int, config: str) -> None:
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
        run_server(host=host, port=port, config_file=config)
    except KeyboardInterrupt:
        click.echo("\nServer stopped by user")
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)


if __name__ == "__main__":
    main()
