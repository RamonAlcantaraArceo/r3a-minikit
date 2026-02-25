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

## Questions?

Feel free to open an issue for questions about contributing.