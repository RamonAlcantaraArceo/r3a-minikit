# Copilot Instructions for r3a-minikit

## Project Overview

r3a-minikit is a Python library providing a collection of reusable utilities and mini modules. It is packaged with Poetry and uses a `src/` layout.

## Project Structure

```
├── .github/
│   └── workflows/ci.yml    # CI pipeline (lint, type-check, test)
├── src/
│   └── r3a_logger/          # Logging utility package
│       ├── __init__.py
│       └── logger.py
├── tests/
│   └── r3a_logger/
│       └── test_logger.py
├── pyproject.toml           # Poetry project config & dev dependencies
└── poetry.lock
```

New packages go under `src/` and their tests under `tests/` mirroring the same directory structure. Each package must be registered in `pyproject.toml` under `packages` (e.g., `{ include = "package_name", from = "src" }`).

## Build & Development

- **Python**: ≥ 3.10
- **Package manager**: Poetry (≥ 2)
- **Install dependencies** (always run first):

  ```bash
  poetry install --with dev
  ```

## Linting, Formatting & Type Checking

Run these commands in order. All must pass before committing:

```bash
poetry run ruff format --check   # Check formatting
poetry run ruff check src/ tests/ # Lint source and tests
poetry run mypy src/ tests/       # Type-check source and tests
```

To auto-fix formatting issues:

```bash
poetry run ruff format
```

## Testing

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Tests use `pytest`. Place test files in `tests/<package_name>/` matching the source layout.

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main`. It executes, in order:

1. `poetry run ruff format --check`
2. `poetry run ruff check src/ tests/`
3. `poetry run mypy src/ tests/`
4. `poetry run pytest --cov=src --cov-report=xml --cov-report=term-missing`

Always replicate this sequence locally before pushing.

## Coding Conventions

- Use type hints on all function signatures.
- Follow docstring style used in the codebase (Google-style Args/Returns).
- Keep `__init__.py` files minimal.
- Use `pathlib.Path` instead of `os.path` for filesystem operations.
