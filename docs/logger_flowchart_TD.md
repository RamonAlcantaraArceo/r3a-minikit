```mermaid
flowchart TD
    get_logger["get_logger"]
    setup_logging["setup_logging"]
    initialize_logging["initialize_logging"]
    get_current_logger["get_current_logger"]
    R3ALogger__init__["R3ALogger.__init__"]
    set_level["R3ALogger.set_level"]
    get_logger_method["R3ALogger.get_logger"]
    cleanup_old_logs["R3ALogger.cleanup_old_logs"]

    get_current_logger --> initialize_logging
    initialize_logging --> setup_logging
    setup_logging --> get_logger
    get_logger --> R3ALogger__init__
    get_current_logger --> get_logger_method
    get_logger_method --> get_logger
    get_logger --> get_logger_method
    get_logger_method --> get_logger
    get_logger --> set_level
    get_logger --> cleanup_old_logs
```