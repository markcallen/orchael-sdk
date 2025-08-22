# Orchael SDK Test Suite

This directory contains comprehensive tests for the Orchael SDK, covering all major components including the CLI functionality.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── test_chat_types.py          # Tests for chat type definitions
├── test_orchael_chat_processor.py  # Tests for the base processor class
├── test_cli.py                 # Tests for CLI functionality
├── test_main_package.py        # Tests for main package functionality
├── test_example_processors.py  # Tests for example processors
└── README.md                   # This file
```

## Running Tests

### Prerequisites

Install the development dependencies:

```bash
pip install -e .[dev]
```

Or if using uv:

```bash
uv sync --group dev
```

### Running All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=orchael_sdk --cov-report=html
```

### Running Specific Test Files

```bash
# Test only chat types
pytest tests/test_chat_types.py

# Test only CLI functionality
pytest tests/test_cli.py

# Test only example processors
pytest tests/test_example_processors.py
```

### Running Tests with Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

The test suite covers:

### Core Components
- **Chat Types** (`test_chat_types.py`): Tests for `ChatInput`, `ChatOutput`, `ChatHistoryEntry`, and `ChatError`
- **Base Processor** (`test_orchael_chat_processor.py`): Tests for the abstract `OrchaelChatProcessor` class
- **Main Package** (`test_main_package.py`): Tests for package-level functionality

### CLI Functionality (`test_cli.py`)
- **Processor Class Loading**: Dynamic loading of processor classes from string paths
- **Configuration Loading**: YAML config file parsing and validation
- **Environment Variable Management**: Setting env vars from config
- **Main CLI Function**: End-to-end CLI execution testing
- **Error Handling**: Proper error handling and exit codes

### Example Processors (`test_example_processors.py`)
- **Echo Processor**: Tests for the example echo processor with various configurations
- **Ollama Processor**: Basic import and inheritance tests
- **Environment Variable Integration**: Testing processor configuration via environment variables

## Test Fixtures

The `conftest.py` file provides several useful fixtures:

- `temp_config_file`: Creates temporary YAML config files for testing
- `sample_chat_input`: Sample chat input data
- `sample_chat_history`: Sample chat history data
- `clean_env`: Manages environment variables during tests
- `examples_path`: Path to the examples directory

## Mocking and Testing Strategy

The tests use extensive mocking to isolate components:

- **Module Imports**: Mocked to test dynamic loading without actual dependencies
- **File System**: Temporary files for config testing
- **Environment Variables**: Controlled environment for processor testing
- **External Dependencies**: Mocked to avoid external service calls

## CLI Testing Approach

CLI tests use a combination of:

1. **Unit Tests**: Testing individual CLI functions in isolation
2. **Integration Tests**: Testing the full CLI workflow
3. **Mock Testing**: Using `unittest.mock` to simulate Click context and user input
4. **Error Path Testing**: Testing various failure scenarios

## Coverage Goals

The test suite aims for:

- **100% Line Coverage**: All code paths should be tested
- **100% Branch Coverage**: All conditional branches should be tested
- **Error Path Coverage**: All error conditions should be tested
- **CLI Coverage**: All CLI options and workflows should be tested

## Configuration

The pytest configuration is defined in `pyproject.toml` under the `[tool.pytest.ini_options]` section, following modern Python project standards.

## Running Tests in CI/CD

For continuous integration, the tests can be run with:

```bash
# Install dependencies
pip install -e .[dev]

# Run tests with coverage
pytest --cov=orchael_sdk --cov-report=xml --cov-report=term-missing

# Run type checking
mypy orchael_sdk/

# Run linting
ruff check orchael_sdk/ tests/
```

## Debugging Tests

To debug failing tests:

```bash
# Run with maximum verbosity
pytest -vvv

# Run a specific test with debugging
pytest tests/test_cli.py::TestLoadProcessorClass::test_load_valid_processor_class -s

# Run with print statement output
pytest -s

# Run with pdb on failures
pytest --pdb
```

## Adding New Tests

When adding new tests:

1. **Follow Naming Convention**: Use `test_*.py` for test files
2. **Use Descriptive Names**: Test methods should clearly describe what they test
3. **Add Type Annotations**: All test methods should have return type annotations
4. **Use Fixtures**: Leverage existing fixtures or create new ones in `conftest.py`
5. **Mock External Dependencies**: Don't rely on external services or files
6. **Test Error Cases**: Include tests for failure scenarios
7. **Add Documentation**: Document complex test scenarios

## Test Dependencies

The test suite requires:

- `pytest`: Core testing framework
- `pytest-cov`: Coverage reporting
- `PyYAML`: For config file testing
- `unittest.mock`: For mocking (built-in with Python 3.3+)

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running tests from the project root
2. **Missing Dependencies**: Install dev dependencies with `pip install -e .[dev]`
3. **Path Issues**: Tests use relative paths, ensure correct working directory
4. **Environment Variables**: Tests clean up environment variables, but conflicts may occur

### Getting Help

If you encounter issues:

1. Check that all dependencies are installed
2. Verify you're in the correct directory
3. Run tests with verbose output: `pytest -v`
4. Check the test output for specific error messages
