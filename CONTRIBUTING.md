# Contributing to r3a-minikit

Thank you for considering contributing to r3a-minikit! This is Ramon's personal utility collection, shared for community benefit.

## ⚠️ Important Note

This software is provided **"as is"** without warranty of any kind. The maintainer is not responsible for any issues arising from its use.

## How to Contribute

### Bug Reports
- Search existing issues before creating new ones
- Provide clear reproduction steps
- Include system information (Python version, OS, etc.)

### Feature Requests
- Explain the use case and why it would be valuable
- Keep in mind this is a personal utility collection
- Simple utilities are preferred over complex frameworks

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the development workflow in README.md
4. Ensure all tests pass and coverage is 100%
5. Run the full CI check sequence locally:
   ```bash
   poetry run ruff format
   poetry run ruff check src/ tests/
   poetry run mypy src/ tests/
   poetry run pytest --cov=src --cov-report=term-missing
   ```
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Standards

- **Test coverage** is required
- **Type hints** for all public APIs
- **Google-style docstrings** for all functions and classes
- **Backward compatibility** should be maintained when possible
- Follow the existing code style and patterns

## Code Review Process

- The maintainer will review PRs when possible
- Community feedback is welcome
- Simple, focused changes are more likely to be accepted
- Large architectural changes should be discussed in an issue first

## Version Management

This project uses [bump2version](https://github.com/c4urself/bump2version) for automated version management.

### Installing bump2version

```bash
pip install bump2version
```

### Version Bumping

To bump versions, use one of these commands:

```bash
# Patch version bump (e.g., 0.0.1 → 0.0.2 for bug fixes)
bump2version patch

# Minor version bump (e.g., 0.1.0 → 0.2.0 for new features)
bump2version minor

# Major version bump (e.g., 1.0.0 → 2.0.0 for breaking changes)
bump2version major
```

**What happens automatically:**
- Updates version in `pyproject.toml`
- Updates `CHANGELOG.md` with new version section
- Creates a git commit with version bump message
- Creates a git tag (e.g., `v0.0.2`)

### Manual Version Changes

If you need to manually modify the version:
1. Update `pyproject.toml`
2. Update `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
3. Commit changes
4. Create annotated tag: `git tag -a v0.0.2 -m "Release v0.0.2"`

## Release Process

### Prerequisites

1. **Ensure you're on main branch with clean working directory**
   ```bash
   git checkout main
   git pull origin main
   git status  # Should be clean
   ```

2. **All changes must be committed and pushed**

3. **All CI checks must be passing**

### Creating a Release

#### Step 1: Prepare Release Branch

1. **Create a release branch**:
   ```bash
   git checkout -b release/v0.0.2  # Use actual version number
   ```

2. **Update changelog** (if needed):
   - Add changes under `[Unreleased]` section in `CHANGELOG.md`
   - Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format

3. **Make any final release preparations** (documentation updates, etc.)

4. **Commit and push release branch**:
   ```bash
   git add .
   git commit -m "Prepare release v0.0.2"
   git push origin release/v0.0.2
   ```

#### Step 2: Create and Review Pull Request

5. **Create PR for release branch**:
   ```bash
   gh pr create --title "Release v0.0.2" --body "Release preparation for v0.0.2"
   ```
   Or create manually on GitHub: `release/v0.0.2` → `main`

6. **Review the PR**:
   - ✅ Ensure all CI checks pass
   - ✅ Review changelog entries
   - ✅ Verify all intended changes are included
   - ✅ Test critical functionality if needed

7. **Merge the PR** once approved

#### Step 3: Create Release

8. **Return to main and pull latest**:
   ```bash
   git checkout main
   git pull origin main
   ```

9. **Bump the version** (creates commit and tag):
   ```bash
   # For bug fixes
   bump2version patch
   
   # For new features  
   bump2version minor
   
   # For breaking changes
   bump2version major
   ```

10. **Push the tag**:
    ```bash
    git push origin main --tags
    ```

11. **Trigger GitHub Release**:
    - Go to [Actions tab](https://github.com/RamonAlcantaraArceo/r3a-minikit/actions)
    - Click "Release" workflow
    - Click "Run workflow"
    - Enter the tag name (e.g., `v0.0.2`)
    - Click "Run workflow"

12. **Verify the release**:
    - Check the [Releases page](https://github.com/RamonAlcantaraArceo/r3a-minikit/releases)
    - Verify the changelog excerpt appears in release notes
    - Test installation: `pip install git+https://github.com/RamonAlcantaraArceo/r3a-minikit.git@v0.0.2`

13. **Clean up**:
    ```bash
    git branch -d release/v0.0.2        # Delete local branch
    git push origin --delete release/v0.0.2  # Delete remote branch
    ```

### Release Workflow

The release workflow automatically:
- Validates the tag exists
- Runs full test suite (format, lint, type check, tests)
- Builds the package with Poetry
- Extracts changelog section for release notes
- Creates GitHub release with built artifacts (.tar.gz and .whl files)
- Publishes release notes from changelog

### Emergency Fixes

For urgent patches to existing releases:
1. Create a branch from the release tag: `git checkout -b hotfix/urgent-fix v0.0.1`  
2. Make minimal fix and test thoroughly
3. Follow normal release process with patch bump
4. Merge hotfix back to main if needed

## Questions?

Feel free to open an issue for questions about contributing.