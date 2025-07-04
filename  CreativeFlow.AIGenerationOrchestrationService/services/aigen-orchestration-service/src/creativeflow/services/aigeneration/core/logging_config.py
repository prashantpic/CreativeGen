"""
logging_config.py

Configuration for application-wide logging.

This module sets up structured logging for the application, with support
for different formats (JSON, text) and log levels configured via environment variables.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON log formatter to add standard attributes.
    """
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        # In a real application, a middleware would inject 'correlation_id'
        # into a context var, which could be accessed here.
        # from contextvars import ContextVar
        # correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default=None)
        # log_record['correlation_id'] = correlation_id_var.get()


def setup_logging(log_level: str = "INFO", log_format: str = "json"):
    """
    Configures the root logger for the application.

    Args:
        log_level (str): The minimum log level to output (e.g., "INFO", "DEBUG").
        log_format (str): The format for logs ("json" or "text").
    """
    log_level_upper = log_level.upper()
    numeric_level = getattr(logging, log_level_upper, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create a handler to stream logs to stdout
    handler = logging.StreamHandler(sys.stdout)

    # Set the formatter based on the configuration
    if log_format.lower() == "json":
        # Example format: timestamp, level, name, message, plus any extra fields
        formatter = CustomJsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
    else:
        # Standard text format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Set log levels for third-party libraries that are too verbose
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)

    # Log that logging has been configured
    root_logger.info(
        "Logging configured successfully with level=%s and format=%s",
        log_level_upper,
        log_format
    )