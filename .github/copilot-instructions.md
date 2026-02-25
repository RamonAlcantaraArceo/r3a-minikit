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
- **Aim for 100% test coverage** - add tests for edge cases, error conditions, and singleton behaviors.
- **Test parameter variations** - when functions have optional parameters, test both default and custom values.
- **Test backward compatibility** - ask if backward compatibility is desired; if so, ensure existing functionality continues to work after refactoring.
- **Use isolated test environments** - employ `tmp_path` fixtures and reset global state between tests.

---

## API Design Guidelines

When developing or refactoring public APIs:

- **Required vs Optional Parameters**: Make essential parameters required (like `log_dir` for file operations), provide sensible defaults for convenience parameters.
- **Backward Compatibility**: When backward compatibility is desired when adding parameters, use defaults that preserve existing behavior. Ask if backward compatibility is a concern before making breaking changes.
- **Singleton Patterns**: Document singleton behavior clearly and test that instances are reused appropriately.
- **Parameter Documentation**: Document not just what parameters do, but their default values and behavioral implications.
- **Behavior Nuances**: Document non-obvious behaviors (e.g., initialization messages always logged at INFO level).

---

## Documentation Standards

- **Docstring Completeness**: Document all parameters, return values, and any side effects.
- **Behavioral Notes**: Add "Note:" sections for non-obvious behaviors or implementation details.
- **Default Value Clarification**: When functions use other functions' defaults, document what those defaults are.
- **Edge Case Documentation**: Document special cases, error conditions, and unusual parameter combinations.

---

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main`. It executes, in order:

1. `poetry run ruff format --check`
2. `poetry run ruff check src/ tests/`
3. `poetry run mypy src/ tests/`
4. `poetry run pytest --cov=src --cov-report=xml --cov-report=term-missing --junitxml=junit.xml`

After tests complete, the CI automatically uploads:
- **Coverage reports** to [Codecov](https://codecov.io) for coverage tracking and PR analysis
- **Test results** to Codecov for test failure analysis and trends

Replicate this sequence locally before pushing. While coverage upload requires CI secrets, you can monitor local coverage with `--cov-report=term-missing`.

---

## Coding Conventions

- Use **type hints everywhere**.
- Use **Google-style docstrings** for all public functions and classes.
- Prefer **dataclasses** when appropriate.
- Use **f-strings** instead of `str.format()`.
- Keep `__init__.py` files minimal.
- Use `pathlib.Path` instead of `os.path` for filesystem operations.
- Prefer pytest idioms over unittest patterns.

---

## Development Workflow

When adding or modifying packages:

1. **Make changes** to source code with proper type hints and docstrings
2. **Add/update tests** to maintain 100% coverage and test edge cases
3. **Run the full check sequence**:
   ```bash
   poetry run ruff format
   poetry run ruff check src/ tests/
   poetry run mypy src/ tests/
   poetry run pytest --cov=src --cov-report=term-missing
   ```
4. **Update documentation** if public APIs change
5. **Test backward compatibility** if modifying existing functions

**Remember**: All CI checks must pass before committing. When in doubt, run the full test suite and linting checks locally first.

