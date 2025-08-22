#!/usr/bin/env python3
"""
Test runner script for orchael-sdk
"""

import subprocess
import sys
import os
import importlib.util


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def main() -> None:
    """Main test runner function"""
    print("🧪 Orchael SDK Test Runner")
    print("=" * 60)

    # Check if we're in the right directory
    if not os.path.exists("orchael_sdk"):
        print("❌ Error: Please run this script from the orchael-sdk root directory")
        sys.exit(1)

    # Check if pytest is available
    try:
        import pytest

        print(f"✅ pytest {pytest.__version__} is available")
    except ImportError:
        print("❌ pytest is not installed. Installing dev dependencies...")
        if not run_command(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            "Installing dev dependencies",
        ):
            print("❌ Failed to install dev dependencies")
            sys.exit(1)

    # Run tests
    success = True

    # Run unit tests
    if not run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], "Unit tests"
    ):
        success = False

    # Run tests with coverage
    if not run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "--cov=orchael_sdk",
            "--cov-report=term-missing",
            "--cov-report=html",
        ],
        "Tests with coverage",
    ):
        success = False

    # Run type checking
    if importlib.util.find_spec("mypy") is not None:
        if not run_command(
            [sys.executable, "-m", "mypy", "orchael_sdk/"], "Type checking"
        ):
            success = False
    else:
        print("⚠️  mypy not available, skipping type checking")

    # Run linting
    if importlib.util.find_spec("ruff") is not None:
        if not run_command(
            [sys.executable, "-m", "ruff", "check", "orchael_sdk/", "tests/"],
            "Linting with ruff",
        ):
            success = False
    else:
        print("⚠️  ruff not available, skipping linting")

    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests and checks completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests or checks failed. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
