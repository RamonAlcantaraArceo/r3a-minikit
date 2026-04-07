"""Logging utilities for r3a-minikit."""

import io
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Default format strings
DEFAULT_FILE_FORMAT: Tuple[str, str] = (
    "%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
DEFAULT_CONSOLE_FORMAT: Tuple[str, str] = (
    "%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s",
    "%H:%M:%S",
)

# Global singleton instance for logger management
_instance: Optional["R3ALogger"] = None


class R3ALogger:
    """Custom logger for r3a-minikit with file and console logging.

    By default, this class also patches the root logger with equivalent
    handlers so records from module and third-party loggers are captured.
    You can disable that behavior with patch_root_logger=False and still add
    module-specific handlers for advanced routing or filtering.
    """

    def __init__(
        self,
        log_dir: Path,
        log_level: str = "INFO",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console_logging: bool = False,
        logger_name: str = "r3a-minikit",
        log_file_name: Optional[str] = None,
        file_format: Tuple[str, str] = DEFAULT_FILE_FORMAT,
        console_format: Tuple[str, str] = DEFAULT_CONSOLE_FORMAT,
        patch_root_logger: bool = True,
    ):
        """Initialize the logger.

        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            max_file_size: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            console_logging: Whether to enable console logging (default: False)
            logger_name: Name for the logger instance (default: "r3a-minikit")
            log_file_name: Optional log file name. If not set, uses logger_name
                + ".log".
            file_format: Tuple of (format_string, datefmt) for file output
            console_format: Tuple of (format_string, datefmt) for console output
            patch_root_logger: Whether to also attach handlers to the root logger
                for compatibility with module and third-party loggers (default:
                True).
        """
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.console_logging = console_logging
        self.logger_name = logger_name
        self.log_file_name = log_file_name or f"{self.logger_name}.log"
        self.patch_root_logger = patch_root_logger

        # Create logs directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.log_level)
        # Prevent duplicates when shared handlers are also attached to root.
        self.logger.propagate = False

        # Clear any existing handlers
        self.logger.handlers.clear()

        # Create formatters
        self.file_formatter = logging.Formatter(
            file_format[0],
            datefmt=file_format[1],
        )

        self.console_formatter = logging.Formatter(
            console_format[0],
            datefmt=console_format[1],
        )

        # Setup file logging with rotation
        log_file = self.log_dir / self.log_file_name
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(file_handler)

        # Setup console logging if enabled
        if self.console_logging:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(self.console_formatter)
            self.logger.addHandler(console_handler)

        if self.patch_root_logger:
            self._patch_root_logger_handlers()

    def _patch_root_logger_handlers(self) -> None:
        """Attach this logger's handlers to root logger without duplicates."""
        root_logger = logging.getLogger()
        root_logger.setLevel(min(root_logger.level, self.log_level))

        existing_keys = {
            self._handler_identity(handler) for handler in root_logger.handlers
        }

        for handler in self.logger.handlers:
            handler_key = self._handler_identity(handler)
            if handler_key in existing_keys:
                continue
            root_logger.addHandler(handler)
            existing_keys.add(handler_key)

    @staticmethod
    def _handler_identity(handler: logging.Handler) -> tuple[str, str]:
        """Build a stable key used to detect equivalent root handlers."""
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            return ("file", str(Path(handler.baseFilename).resolve()))

        if isinstance(handler, logging.StreamHandler):
            stream = handler.stream
            if isinstance(stream, io.TextIOBase):
                stream_name = getattr(stream, "name", None)
                if stream_name is not None:
                    return ("stream", str(stream_name))
                return ("stream", str(id(stream)))
            return ("stream", str(id(stream)))

        return ("handler", handler.__class__.__name__)

    def set_level(self, log_level: str) -> None:
        """Change the logging level.

        Args:
            log_level: New logging level (DEBUG, INFO, WARNING, ERROR)
        """
        level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

        if self.patch_root_logger:
            root_logger = logging.getLogger()
            root_logger.setLevel(min(root_logger.level, level))

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance.

        Returns:
            The logger instance
        """
        return self.logger

    def cleanup_old_logs(self, days: int = 30) -> None:
        """Clean up log files older than specified days.

        Args:
            days: Number of days to keep log files
        """
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for log_file in self.log_dir.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                self.logger.info(f"Cleaned up old log file: {log_file.name}")


def get_logger(
    log_dir: Path,
    log_level: str = "INFO",
    console_logging: bool = False,
    logger_name: str = "r3a-minikit",
    log_file_name: Optional[str] = None,
    file_format: Tuple[str, str] = DEFAULT_FILE_FORMAT,
    console_format: Tuple[str, str] = DEFAULT_CONSOLE_FORMAT,
    patch_root_logger: bool = True,
) -> logging.Logger:
    """Get a configured logger instance.

    Args:
        log_dir: Directory for log files
        log_level: Logging level
        console_logging: Whether to enable console logging
        patch_root_logger: Whether to also patch the root logger handlers

    Returns:
        Configured logger instance
    """
    # Use a global instance to avoid multiple handlers
    global _instance
    if _instance is None:
        _instance = R3ALogger(
            log_dir=log_dir,
            log_level=log_level,
            console_logging=console_logging,
            logger_name=logger_name,
            log_file_name=log_file_name,
            file_format=file_format,
            console_format=console_format,
            patch_root_logger=patch_root_logger,
        )

    return _instance.get_logger()


def setup_logging(
    log_dir: Path,
    log_level: str = "INFO",
    console_logging: bool = False,
    logger_name: str = "r3a-minikit",
    log_file_name: Optional[str] = None,
    file_format: Tuple[str, str] = DEFAULT_FILE_FORMAT,
    console_format: Tuple[str, str] = DEFAULT_CONSOLE_FORMAT,
    patch_root_logger: bool = True,
) -> logging.Logger:
    """Setup and configure logging for r3a-minikit.

    Args:
        log_dir: Directory for log files
        log_level: Logging level
        console_logging: Whether to enable console logging (default: False)
        logger_name: Name for the logger instance (default: "r3a-minikit")
        log_file_name: Optional log file name. If None, uses logger_name + ".log"
        file_format: Tuple of (format_string, datefmt) for file output
        console_format: Tuple of (format_string, datefmt) for console output
        patch_root_logger: Whether to also patch the root logger handlers

    Returns:
        Configured logger instance
    """
    # Clear any existing global instance
    global _instance
    _instance = None

    return get_logger(
        log_dir,
        log_level,
        console_logging,
        logger_name,
        log_file_name,
        file_format,
        console_format,
        patch_root_logger,
    )


def initialize_logging(
    log_dir: Path,
    log_level: str = "INFO",
    console_logging: bool = False,
    logger_name: str = "r3a-minikit",
    log_file_name: Optional[str] = None,
    file_format: Tuple[str, str] = DEFAULT_FILE_FORMAT,
    console_format: Tuple[str, str] = DEFAULT_CONSOLE_FORMAT,
    patch_root_logger: bool = True,
) -> None:
    """Initialize logging with specified level.

    Note: The initialization message is always logged at INFO level regardless
    of the specified log_level to ensure it's visible during setup. The logger
    is then switched to the desired level after initialization.

    Args:
        log_dir: Directory to store log files
        log_level: Logging level (default: INFO)
        console_logging: Enable console logging (default False)
        logger_name: Name for the logger instance (default: "r3a-minikit")
        log_file_name: Optional log file name. If None, uses logger_name + ".log"
        file_format: Tuple of (format_string, datefmt) for file output
        console_format: Tuple of (format_string, datefmt) for console output
        patch_root_logger: Whether to also patch the root logger handlers
    """

    # Start at INFO level to ensure initialization message is always visible
    logger = setup_logging(
        log_dir=log_dir,
        log_level="INFO",
        console_logging=console_logging,
        logger_name=logger_name,
        log_file_name=log_file_name,
        file_format=file_format,
        console_format=console_format,
        patch_root_logger=patch_root_logger,
    )

    logger.info(f"Logging initialized at {log_level} level")

    # Now switch to the desired level if different from INFO
    if log_level != "INFO":
        if _instance is not None:
            _instance.set_level(log_level)


def get_current_logger(
    log_dir: Optional[Path] = None,
) -> Optional[logging.Logger]:
    """Get the current logger instance.

    Args:
        log_dir: Directory for log files. Defaults to ~/.r3a-minikit/logs

    Returns:
        The current logger instance
    """
    if _instance is None:
        default_log_dir = log_dir or (Path.home() / ".r3a-minikit" / "logs")
        initialize_logging(log_dir=default_log_dir)
    return _instance.get_logger() if _instance else None
