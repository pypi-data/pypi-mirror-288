from .logging_pomes import (
    DEBUG, INFO, WARNING, ERROR, CRITICAL,
    LOGGING_ID, LOGGING_LEVEL, LOGGING_FORMAT, LOGGING_STYLE,
    LOGGING_FILE_PATH, LOGGING_FILE_MODE, PYPOMES_LOGGER,
    logging_startup, logging_get_entries, logging_send_entries,
    logging_log_msgs, logging_log_debug, logging_log_error,
    logging_log_info, logging_log_critical, logging_log_warning,
)

__all__ = [
    # logging_pomes
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL",
    "LOGGING_ID", "LOGGING_LEVEL", "LOGGING_FORMAT", "LOGGING_STYLE",
    "LOGGING_FILE_PATH", "LOGGING_FILE_MODE", "PYPOMES_LOGGER",
    "logging_startup", "logging_get_entries", "logging_send_entries",
    "logging_log_msgs", "logging_log_debug", "logging_log_error",
    "logging_log_info", "logging_log_critical", "logging_log_warning",
]

from importlib.metadata import version
__version__ = version("pypomes_logging")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
