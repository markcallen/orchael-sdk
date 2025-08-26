# Setting Up GitHub Actions for Orchael SDK

This guide will help you set up GitHub Actions to automatically build, test, and publish the Orchael SDK.

## Prerequisites

1. **GitHub Repository**: Ensure your repository is on GitHub
2. **Admin Access**: You need admin access to the repository to set up secrets
3. **PyPI Account**: A PyPI account for publishing packages

## Step 1: Set Up PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Click "Add API token"
3. Give it a name (e.g., "orchael-sdk-publish")
4. Set the scope to "Entire account (all projects)"
5. Copy the token (you won't see it again!)

## Step 2: Add GitHub Repository Secret

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI API token
6. Click "Add secret"

## Step 3: Verify Workflow Files

Ensure these files are in your repository:

```
orchael-sdk/
├── .github/
│   ├── workflows/
│   │   ├── publish.yml      # Build and publish workflow
│   │   ├── test.yml         # Test workflow
│   │   └── security.yml     # Security scanning workflow
│   └── README.md            # Workflow documentation
├── orchael-sdk/
│   ├── pyproject.toml       # Package configuration
│   └── ...
└── ...
```

## Step 4: Test the Setup

### Test the Test Workflow

1. Make a small change to your code
2. Push to a branch
3. Create a pull request
4. Check the Actions tab to see if tests run

### Test the Build Process Locally

```bash
cd orchael-sdk
uv sync --dev
uv run pytest
uv run python -m build
```

## Step 5: Publish Your First Release

### Option 1: Tag-Based Release (Recommended)

1. Update version in `pyproject.toml`:
   ```toml
   [project]
   version = "0.1.0"
   ```

2. Commit and push:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.0"
   git push
   ```

3. Create and push a tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

4. The workflow will automatically:
   - Run tests
   - Build the package
   - Publish to PyPI
   - Create a GitHub release

### Option 2: Manual Release

1. Go to Actions → Build and Publish SDK
2. Click "Run workflow"
3. Enter version: `0.1.0`
4. Set dry_run: `false`
5. Click "Run workflow"

## Step 6: Verify Publication

1. Check PyPI: [https://pypi.org/project/orchael-sdk/](https://pypi.org/project/orchael-sdk/)
2. Check GitHub Releases
3. Test installation:
   ```bash
   pip install orchael-sdk
   orchael-sdk-cli --help
   ```

## Workflow Details

### Test Workflow (`test.yml`)

- **Triggers**: Push to main/develop, pull requests
- **Actions**: Runs tests, linting, and build verification
- **Python versions**: 3.10, 3.11, 3.12

### Publish Workflow (`publish.yml`)

- **Triggers**: Tag pushes, manual dispatch
- **Actions**: Tests → Build → Publish → Release
- **Outputs**: PyPI package, GitHub release

### Security Workflow (`security.yml`)

- **Triggers**: Weekly schedule, push/PR, manual
- **Actions**: Security scanning, dependency updates
- **Outputs**: Security reports, dependency update issues

## Troubleshooting

### Common Issues

1. **Tests failing**: Check test output in Actions tab
2. **Build failing**: Verify `pyproject.toml` configuration
3. **PyPI publishing error**: Check `PYPI_API_TOKEN` secret
4. **Permission denied**: Verify repository permissions

### Debugging Steps

1. Check Actions tab for detailed logs
2. Verify all prerequisites are met
3. Test locally before pushing
4. Check GitHub repository settings

### Getting Help

- Check the Actions tab for error details
- Review the workflow files for configuration
- Ensure all required secrets are set
- Verify the repository structure matches expectations

## Best Practices

1. **Always test locally** before pushing
2. **Use semantic versioning** for releases
3. **Review workflow logs** after each run
4. **Keep dependencies updated** using the security workflow
5. **Monitor PyPI publication** for successful releases

## Advanced Configuration

### Custom Python Versions

Edit the workflow files to change Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]
```

### Additional Testing

Add more test steps to the test workflow:

```yaml
- name: Run additional checks
  run: |
    cd orchael-sdk
    uv run mypy orchael_sdk
    uv run black --check .
    uv run ruff check .
```

### Custom Build Commands

Modify the build process in `publish.yml`:

```yaml
- name: Custom build step
  run: |
    cd orchael-sdk
    # Add custom build logic here
    uv run python -m build
```

## Security Considerations

- PyPI tokens are encrypted and secure
- Workflows only run on trusted code
- Build artifacts are verified before publishing
- Only tagged releases trigger automatic publishing

## Next Steps

1. **Set up branch protection** rules
2. **Configure code review** requirements
3. **Set up automated dependency updates**
4. **Monitor workflow performance**
5. **Customize workflows** for your needs

## Support

If you encounter issues:

1. Check the workflow documentation in `.github/README.md`
2. Review GitHub Actions documentation
3. Check PyPI publishing guidelines
4. Verify your repository configuration
