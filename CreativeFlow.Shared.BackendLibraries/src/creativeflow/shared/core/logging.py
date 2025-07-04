"""
Provides a standardized logging configuration utility for all backend services
to ensure consistent, structured (JSON) logging practices.
"""
import logging
import sys
import json
from contextvars import ContextVar
from typing import Optional, Any

# Context variable to hold the correlation ID for a request
correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class ServiceNameFilter(logging.Filter):
    """Injects the service_name into the log record."""
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name

    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, "service_name", self.service_name)
        return True


class JsonFormatter(logging.Formatter):
    """Formats log records as a single line of JSON."""
    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record into a JSON string.

        Args:
            record: The original log record.

        Returns:
            A JSON string representing the log record.
        """
        log_object: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service_name", "unknown"),
            "correlation_id": correlation_id_var.get(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }

        if record.exc_info:
            log_object["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_object["stack_info"] = self.formatStack(record.stack_info)

        # Include any extra fields passed to the logger
        extra = record.__dict__.get("extra")
        if extra:
            log_object.update(extra)

        return json.dumps(log_object, default=str)


def configure_logging(service_name: str, log_level: str = "INFO") -> None:
    """
    Configures the root logger for structured JSON logging.

    This function should be called once at the application's startup.
    It removes existing handlers to prevent duplicate logs, sets up a
    new handler with a JSON formatter, and adds a filter to inject
    the service name into every log record.

    Args:
        service_name: The name of the service, which will be included in all log records.
        log_level: The minimum log level to output (e.g., "INFO", "DEBUG").
    """
    root_logger = logging.getLogger()

    # Clear any existing handlers to avoid duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Set the log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(level)

    # Create a handler to output to stdout
    handler = logging.StreamHandler(sys.stdout)

    # Add the service name filter
    service_filter = ServiceNameFilter(service_name)
    handler.addFilter(service_filter)

    # Create and set the JSON formatter
    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    # Add the handler to the root logger
    root_logger.addHandler(handler)

    logging.info(f"Structured JSON logging configured for service '{service_name}' at level {log_level.upper()}")