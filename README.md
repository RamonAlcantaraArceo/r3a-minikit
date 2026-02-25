# r3a-minikit

[![codecov](https://codecov.io/gh/RamonAlcantaraArceo/r3a-minikit/graph/badge.svg)](https://codecov.io/gh/RamonAlcantaraArceo/r3a-minikit)
[![CI](https://github.com/RamonAlcantaraArceo/r3a-minikit/actions/workflows/ci.yml/badge.svg)](https://github.com/RamonAlcantaraArceo/r3a-minikit/actions/workflows/ci.yml)

Ramon's personal collection of reusable Python utilities and mini modules for common development tasks.

## Overview

r3a-minikit (where **r3a** stands for **R**amon **A**ntonio **A**lcantara **A**rceo) is my personal toolkit of utilities that solve common programming challenges I encounter regularly. Each module is designed to be lightweight, focused, and easy to integrate into projects.

## Features

### 📝 Logging (`r3a_logger`)
- **File and console logging** with automatic log rotation
- **Custom formatting** for file and console outputs
- **Configurable log levels** with initialization message visibility
- **Singleton pattern** for consistent logger instances
- **Log cleanup utilities** for managing disk space
- **Type-safe** with comprehensive type hints

## Installation

```bash
pip install r3a-minikit
```

## Quick Start

### Logging

```python
from pathlib import Path
from r3a_logger import initialize_logging, get_current_logger

# Initialize logging with custom directory
log_dir = Path("./logs")
initialize_logging(log_dir=log_dir, log_level="INFO", console_logging=True)

# Get logger and start logging
logger = get_current_logger()
logger.info("Application started")
logger.warning("This is a warning")
logger.error("Something went wrong")
```

### Advanced Logging Configuration

```python
from r3a_logger import setup_logging
from pathlib import Path

# Custom logger with file rotation
logger = setup_logging(
    log_dir=Path("./app_logs"),
    log_level="DEBUG", 
    console_logging=True,
    logger_name="my-app",
    log_file_name="application.log"
)

logger.debug("Debug information")
logger.info("Process completed successfully")
```

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

### Setup
```bash
# Clone the repository
git clone https://github.com/RamonAlcantaraArceo/r3a-minikit.git
cd r3a-minikit

# Install dependencies
poetry install --with dev
```

### Running Tests
```bash
# Run tests with coverage
poetry run pytest --cov=src --cov-report=term-missing

# Run specific test file
poetry run pytest tests/r3a_logger/test_logger.py -v
```

### Code Quality
```bash
# Format code
poetry run ruff format

# Lint code
poetry run ruff check src/ tests/

# Type checking
poetry run mypy src/ tests/
```

## Contributing

Contributions are welcome! Please ensure:
- Add test coverage for new features
- Type hints for all public APIs
- Google-style docstrings
- All CI checks pass locally before submitting

## License

[MIT License](LICENSE)
