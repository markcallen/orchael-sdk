# GitHub Actions for Orchael SDK

This directory contains GitHub Actions workflows for building, testing, and publishing the Orchael SDK.

## Workflows

### Build and Publish SDK (`publish.yml`)

This workflow handles the complete CI/CD pipeline for the Orchael SDK:

1. **Testing**: Runs tests across multiple Python versions (3.10, 3.11, 3.12)
2. **Building**: Creates distributable packages (wheel and source distribution)
3. **Publishing**: Publishes to PyPI and creates GitHub releases

## Triggers

The workflow is triggered by:

- **Tag pushes**: Any tag starting with `v*` (e.g., `v0.1.0`, `v1.2.3`)
- **Manual dispatch**: Can be run manually from the Actions tab with custom parameters

## Manual Workflow Dispatch

You can manually trigger the workflow with these inputs:

- **version**: The version to publish (e.g., "0.1.0")
- **dry_run**: Set to `true` to run without actually publishing (default: `false`)

## Prerequisites

### PyPI Publishing

To publish to PyPI, you need to set up a PyPI API token:

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Create an API token
3. Add the token as a GitHub repository secret named `PYPI_API_TOKEN`

### GitHub Permissions

The workflow needs these permissions to create releases:

- `contents: write` - To create GitHub releases
- `packages: write` - To publish packages (if using GitHub Packages)

## Workflow Steps

### Test Job

- Runs on Ubuntu with Python 3.10, 3.11, and 3.12
- Installs dependencies using `uv`
- Runs pytest with coverage
- Uploads coverage reports to Codecov

### Build Job

- Runs after successful tests
- Builds the package using `python -m build`
- Verifies the built package by installing it and testing CLI commands
- Uploads build artifacts for the publish job

### Publish Job

- Runs after successful build
- Downloads build artifacts
- Publishes to PyPI using the official PyPI publish action
- Creates a GitHub release if triggered by a tag

## Package Structure

The workflow expects the following structure:

```
orchael-sdk/
├── .github/
│   └── workflows/
│       └── publish.yml
├── orchael-sdk/
│   ├── pyproject.toml
│   ├── orchael_sdk/
│   └── tests/
└── README.md
```

## Version Management

### Automatic Versioning

When you push a tag like `v0.1.0`, the workflow will:

1. Extract the version from the tag
2. Build the package
3. Publish to PyPI
4. Create a GitHub release

### Manual Versioning

For manual releases:

1. Go to Actions → Build and Publish SDK
2. Click "Run workflow"
3. Enter the version number
4. Choose whether to do a dry run
5. Click "Run workflow"

## Troubleshooting

### Common Issues

1. **Build failures**: Check that `pyproject.toml` is properly configured
2. **Test failures**: Ensure all tests pass locally before pushing
3. **PyPI publishing errors**: Verify `PYPI_API_TOKEN` secret is set correctly
4. **Permission errors**: Check repository permissions and workflow file location

### Debugging

- Check the Actions tab for detailed logs
- Verify all prerequisites are met
- Test the build process locally using `uv run python -m build`

## Local Testing

Before pushing, test the build process locally:

```bash
cd orchael-sdk
uv sync --dev
uv run pytest
uv run python -m build
```

## Security

- The workflow uses official, trusted actions
- PyPI tokens are stored as encrypted secrets
- Build artifacts are verified before publishing
- Only tagged releases trigger automatic publishing
