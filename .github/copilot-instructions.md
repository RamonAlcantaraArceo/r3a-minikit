# ** Copilot Instructions for r3a-minikit**

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

New packages go under `src/` and their tests under `tests/`, mirroring the same directory structure.  
Each package must be registered in `pyproject.toml` under `packages` (e.g., `{ include = "package_name", from = "src" }`).

---

## Build & Development

- **Python**: ≥ 3.14  
- **Package manager**: Poetry (≥ 2)
- Install dependencies:

```bash
poetry install --with dev
```

---

## Linting, Formatting & Type Checking

Run these commands in order. All must pass before committing:

```bash
poetry run ruff format --check
poetry run ruff check src/ tests/
poetry run mypy src/ tests/
```

To auto-fix formatting issues:

```bash
poetry run ruff format
```

After generating or modifying code, always run the formatter and linter.

---

## Testing

Tests use **pytest** (not unittest).  
Place test files in `tests/<package_name>/` using the naming convention:

```
test_*.py
```

Run the full suite with:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

**Testing workflow preferences:**

- Start with the simplest failing test case.
- Keep tests small, focused, and colocated with their corresponding module.
- Use pytest fixtures and idioms rather than unittest-style classes.

---

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main`. It executes, in order:

1. `poetry run ruff format --check`
2. `poetry run ruff check src/ tests/`
3. `poetry run mypy src/ tests/`
4. `poetry run pytest --cov=src --cov-report=xml --cov-report=term-missing`

Replicate this sequence locally before pushing.

---

## Coding Conventions

- Use **type hints everywhere**.
- Use **Google-style docstrings** for all public functions and classes.
- Prefer **dataclasses** when appropriate.
- Use **f-strings** instead of `str.format()`.
- Keep `__init__.py` files minimal.
- Use `pathlib.Path` instead of `os.path` for filesystem operations.
- Prefer pytest idioms over unittest patterns.

