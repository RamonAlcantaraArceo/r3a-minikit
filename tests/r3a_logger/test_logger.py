"""Unit tests for logger.py (R3ALogger and helpers)."""

import logging
import logging.handlers
import os

from r3a_logger.logger import (
    R3ALogger,
    get_current_logger,
    get_logger,
    setup_logging,
)


def test_logger_creates_log_file_and_console(tmp_path):
    log_dir = tmp_path / "logs"
    logger_obj = R3ALogger(log_dir, log_level="DEBUG", console_logging=True)
    logger = logger_obj.get_logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    log_file = log_dir / "r3a-minikit.log"
    assert log_file.exists()
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "debug message" in content
        assert "info message" in content
        assert "warn message" in content
        assert "error message" in content


def test_initialize_logging_debug(tmp_path, monkeypatch):
    from r3a_logger import logger as logger_mod

    logger_mod._instance = None
    log_dir = tmp_path / ".r3a-minikit" / "logs"
    # Call initialize_logging with log_level='DEBUG'
    logger_mod.initialize_logging(
        log_dir=log_dir, log_level="DEBUG", console_logging=True
    )
    log_file = log_dir / "r3a-minikit.log"
    assert log_file.exists()
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "Logging initialized at DEBUG level" in content


def test_logger_respects_log_level(tmp_path):
    log_dir = tmp_path / "logs"
    logger_obj = R3ALogger(log_dir, log_level="WARNING", console_logging=False)
    logger = logger_obj.get_logger()
    logger.debug("should not appear")
    logger.info("should not appear")
    logger.warning("should appear")
    logger.error("should appear")
    log_file = log_dir / "r3a-minikit.log"
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "should not appear" not in content
        assert "should appear" in content


def test_set_level_changes_log_level(tmp_path):
    log_dir = tmp_path / "logs"
    logger_obj = R3ALogger(log_dir, log_level="ERROR", console_logging=False)
    logger = logger_obj.get_logger()
    logger_obj.set_level("DEBUG")
    logger.debug("debug now visible")
    log_file = log_dir / "r3a-minikit.log"
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "debug now visible" in content


def test_cleanup_old_logs(tmp_path):
    log_dir = tmp_path / "logs"
    logger_obj = R3ALogger(log_dir, log_level="INFO", console_logging=False)
    # Create a fake old log file
    old_log = log_dir / "old.log"
    old_log.write_text("old log")
    # Set mtime to 40 days ago
    old_time = os.path.getmtime(old_log) - (40 * 24 * 60 * 60)
    os.utime(old_log, (old_time, old_time))
    logger_obj.cleanup_old_logs(days=30)
    assert not old_log.exists()


def test_get_logger_and_setup_logging(tmp_path):
    log_dir = tmp_path / "logs"
    logger1 = get_logger(log_dir, log_level="INFO", console_logging=False)
    logger2 = get_logger(log_dir, log_level="DEBUG", console_logging=False)
    assert logger1 is logger2  # Should be singleton
    logger3 = setup_logging(log_dir, log_level="DEBUG", console_logging=False)
    assert logger3 is not None
    assert logger3 is get_logger(log_dir, log_level="DEBUG", console_logging=False)


def test_get_current_logger_returns_logger(tmp_path):
    # Remove global _instance if set
    from r3a_logger import logger as logger_mod

    logger_mod._instance = None
    log_dir = tmp_path / ".r3a-minikit" / "logs"
    logger_mod.initialize_logging(log_dir=log_dir)
    log = get_current_logger()
    assert isinstance(log, logging.Logger)


def test_custom_format_tuples(tmp_path):
    """Test that custom format tuples work correctly."""
    log_dir = tmp_path / "logs"

    # Define custom formats
    custom_file_format = ("[%(asctime)s] %(levelname)s: %(message)s", "%Y/%m/%d %H:%M")
    custom_console_format = ("%(levelname)s - %(message)s", "%H:%M:%S")

    # Create logger with custom formats
    logger_obj = R3ALogger(
        log_dir,
        log_level="INFO",
        console_logging=True,
        file_format=custom_file_format,
        console_format=custom_console_format,
    )

    logger = logger_obj.get_logger()
    logger.info("Test message with custom format")
    logger.warning("Warning with custom format")

    # Check file format
    log_file = log_dir / "r3a-minikit.log"
    assert log_file.exists()
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        # Should contain custom file format pattern
        assert "[202" in content  # Year format
        assert "INFO:" in content  # Level format from custom pattern
        assert "WARNING:" in content
        assert "Test message with custom format" in content
        # Should NOT contain the default format patterns
        assert " | " not in content  # Default separator

    # Verify formatters are using custom formats
    file_handler = None
    console_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            file_handler = handler
        elif isinstance(handler, logging.StreamHandler):
            console_handler = handler

    assert file_handler is not None
    assert console_handler is not None

    assert file_handler.formatter is not None
    assert console_handler.formatter is not None

    # Check that formatters have the custom format strings
    assert file_handler.formatter._fmt == custom_file_format[0]
    assert file_handler.formatter.datefmt == custom_file_format[1]
    assert console_handler.formatter._fmt == custom_console_format[0]
    assert console_handler.formatter.datefmt == custom_console_format[1]


def test_helper_functions_with_custom_formats(tmp_path, monkeypatch):
    """Test that helper functions work with custom format tuples."""
    from r3a_logger import logger as logger_mod

    logger_mod._instance = None

    log_dir = tmp_path / "logs"
    custom_file_format = ("%(levelname)s:%(message)s", "%Y%m%d")
    custom_console_format = ("%(message)s", "%H%M%S")

    # Test get_logger with custom formats
    logger1 = get_logger(
        log_dir,
        log_level="INFO",
        console_logging=True,
        file_format=custom_file_format,
        console_format=custom_console_format,
    )
    logger1.info("Test from get_logger")

    # Test setup_logging with custom formats
    logger_mod._instance = None
    logger2 = setup_logging(
        log_dir,
        log_level="INFO",
        console_logging=True,
        file_format=custom_file_format,
        console_format=custom_console_format,
    )
    logger2.info("Test from setup_logging")

    # Test initialize_logging with custom formats
    logger_mod._instance = None
    init_log_dir = tmp_path / ".r3a-minikit" / "logs"
    logger_mod.initialize_logging(
        log_dir=init_log_dir,
        log_level="INFO",
        console_logging=True,
        file_format=custom_file_format,
        console_format=custom_console_format,
    )
    logger3 = logger_mod.get_current_logger()
    assert logger3 is not None
    logger3.info("Test from initialize_logging")

    # Verify all logs use custom format
    log_file = init_log_dir / "r3a-minikit.log"
    assert log_file.exists()
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        # Should use custom format (level:message, no timestamps due to date format)
        assert "INFO:Logging initialized" in content
        assert "INFO:Test from initialize_logging" in content
        # Should NOT contain default format patterns
        assert " | " not in content


def test_get_current_logger_with_custom_log_dir(tmp_path):
    """Test get_current_logger with custom log_dir parameter."""
    from r3a_logger import logger as logger_mod

    # Reset global instance
    logger_mod._instance = None

    custom_log_dir = tmp_path / "custom_logs"

    # Call get_current_logger with custom directory
    logger = get_current_logger(log_dir=custom_log_dir)

    # Verify logger was created
    assert logger is not None
    assert isinstance(logger, logging.Logger)

    # Log a message
    logger.info("Test message from custom directory")

    # Verify log file was created in custom directory
    log_file = custom_log_dir / "r3a-minikit.log"
    assert log_file.exists()

    # Verify log content
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "Test message from custom directory" in content


def test_get_current_logger_default_behavior(tmp_path, monkeypatch):
    """Test get_current_logger default behavior (uses ~/.r3a-minikit/logs)."""
    from r3a_logger import logger as logger_mod

    # Patch Path.home to tmp_path for isolation
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    # Reset global instance
    logger_mod._instance = None

    # Call get_current_logger without parameters
    logger = get_current_logger()

    # Verify logger was created
    assert logger is not None
    assert isinstance(logger, logging.Logger)

    # Log a message
    logger.info("Test message from default directory")

    # Verify log file was created in default directory
    default_log_dir = tmp_path / ".r3a-minikit" / "logs"
    log_file = default_log_dir / "r3a-minikit.log"
    assert log_file.exists()

    # Verify log content
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "Test message from default directory" in content


def test_get_current_logger_singleton_behavior(tmp_path):
    """Test that get_current_logger returns the same instance."""
    from r3a_logger import logger as logger_mod

    # Reset global instance
    logger_mod._instance = None

    custom_log_dir = tmp_path / "singleton_test"

    # Get logger first time
    logger1 = get_current_logger(log_dir=custom_log_dir)

    # Get logger second time (should be same instance, even with different log_dir)
    logger2 = get_current_logger(log_dir=tmp_path / "different_dir")

    # They should be the same logger instance (singleton behavior)
    assert logger1 is logger2

    # Also test calling without log_dir after initialization
    logger3 = get_current_logger()
    assert logger1 is logger3


def test_get_current_logger_preserves_existing_instance(tmp_path):
    """Test that get_current_logger preserves existing logger instance."""
    from r3a_logger import logger as logger_mod

    # Reset global instance
    logger_mod._instance = None

    # Initialize logging first with specific settings
    log_dir = tmp_path / "preserve_test"
    logger_mod.initialize_logging(
        log_dir=log_dir, log_level="DEBUG", console_logging=True
    )

    # Get the current logger after initialization
    logger = get_current_logger()

    # Verify it's the same instance that was created by initialize_logging
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG  # Verify it preserved the DEBUG level

    # Verify calling with different log_dir doesn't change the instance
    logger2 = get_current_logger(log_dir=tmp_path / "different")
    assert logger is logger2


def test_initialize_logging_with_custom_logger_name_and_file(tmp_path):
    """Test initialize_logging with custom logger_name and log_file_name."""
    from r3a_logger import logger as logger_mod

    # Reset global instance
    logger_mod._instance = None

    log_dir = tmp_path / "custom_logger_test"

    # Initialize logging with custom logger name and file name
    logger_mod.initialize_logging(
        log_dir=log_dir,
        log_level="INFO",
        console_logging=True,
        logger_name="custom-logger",
        log_file_name="my-app.log",
    )

    # Verify log file was created with custom name
    log_file = log_dir / "my-app.log"
    assert log_file.exists()

    # Verify log content
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "Logging initialized at INFO level" in content

    # Verify logger name is correct
    logger = logger_mod.get_current_logger()
    assert logger is not None
    assert logger.name == "custom-logger"


def test_initialize_logging_with_default_log_file_name(tmp_path):
    """Test initialize_logging uses logger_name.log when log_file_name is None."""
    from r3a_logger import logger as logger_mod

    # Reset global instance
    logger_mod._instance = None

    log_dir = tmp_path / "default_file_test"

    # Initialize logging with custom logger name but default file name
    logger_mod.initialize_logging(
        log_dir=log_dir,
        log_level="INFO",
        logger_name="my-service",
        # log_file_name=None (default)
    )

    # Verify log file was created with logger_name + ".log"
    log_file = log_dir / "my-service.log"
    assert log_file.exists()

    # Verify log content
    with open(log_file, encoding="utf-8") as f:
        content = f.read()
        assert "Logging initialized at INFO level" in content
