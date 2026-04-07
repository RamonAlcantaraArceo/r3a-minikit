# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2026-04-07

### Added
- **Root Logger Compatibility** (`R3ALogger`): New `patch_root_logger` parameter (default `True`) attaches the file and console handlers to the root logger so records from module loggers (`logging.getLogger(__name__)`) and third-party libraries are automatically captured in the log file and console output.
- **Propagation Control**: Named logger `propagate` is set to `False` when root patching is active, preventing duplicate log entries.
- **Level Synchronization**: Root logger level is kept at or below the named logger level; `set_level()` now updates the root level in sync.

### Changed
- `initialize_logging()`: Level transition after the init message now delegates to `set_level()` so root level stays consistent.

### Released
- **Changelog Extraction**: Improved awk script to properly extract release notes without including reference links
- **Release Notes**: Clean extraction of changelog sections for GitHub releases without footer links

## [0.0.1] - 2026-02-25

### Added
- Initial release of r3a-minikit
- `r3a_logger` package with comprehensive logging utilities
- `R3ALogger` class for file and console logging with rotation
- `initialize_logging()` function for simple setup
- `setup_logging()` function for flexible configuration  
- `get_current_logger()` and `get_logger()` functions for accessing logger instances
- Support for Python 3.10-3.14
- Comprehensive test suite with 100% coverage
- Multi-version testing with tox
- CI/CD pipeline with GitHub Actions
- Code quality enforcement with Ruff and Mypy
- Coverage reporting with Codecov

## [0.0.1-beta.3] - 2026-02-25

### 🧪 Testing Release Infrastructure
- **Release Workflow**: Fixed GitHub Actions permissions (403 error resolved)
- **Token Handling**: Upgraded to `softprops/action-gh-release@v2` with improved token support
- **Prerelease Detection**: Auto-detection of prereleases (beta, alpha, rc) via tag name pattern  
- **Changelog Integration**: Testing changelog extraction for release notes ✅
- **Build Process**: Verified package builds correctly with Poetry
- **CI Validation**: Full test suite passes (linting, type checking, 100% coverage)

### 🎯 What's Being Tested
- GitHub release creation with proper permissions
- Change log content extraction and formatting
- Package artifact generation (`.tar.gz` and `.whl` files)
- Prerelease marking for beta versions

This is a **beta release** to validate the complete release infrastructure before the official v0.0.1 release.


[Unreleased]: https://github.com/RamonAlcantaraArceo/r3a-minikit/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/RamonAlcantaraArceo/r3a-minikit/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/RamonAlcantaraArceo/r3a-minikit/releases/tag/v0.0.1
[0.0.1-beta.3]: https://github.com/RamonAlcantaraArceo/r3a-minikit/releases/tag/v0.0.1-beta.3