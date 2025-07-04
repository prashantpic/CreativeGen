"""
Provides standardized logging configuration for all Python services.
This module sets up structured JSON logging using `python-json-logger`
and manages correlation IDs using `contextvars` for request tracing.

Requirement Mapping: DEP-005 (Standardized Log Format)
"""
import contextvars
import datetime
import logging
import sys

from python_json_logger import formatter

# Context variable to hold the correlation ID for the current async context.
_correlation_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)


def add_correlation_id(correlation_id: str) -> contextvars.Token:
    """
    Sets the correlation ID for the current context.

    Typically called by a middleware at the beginning of a request.

    Args:
        correlation_id: The ID to set for the current request/context.

    Returns:
        A token that can be used to reset the context variable.
    """
    return _correlation_id_var.set(correlation_id)


def get_correlation_id() -> str | None:
    """
    Retrieves the correlation ID from the current context.

    Returns:
        The current correlation ID, or None if it's not set.
    """
    return _correlation_id_var.get()


def setup_logging(
    service_name: str, log_level: str = "INFO", environment: str = "development"
) -> None:
    """
    Configures the root logger for structured JSON logging.

    This function should be called once at application startup.

    Args:
        service_name: The name of the microservice.
        log_level: The minimum log level to output (e.g., 'INFO', 'DEBUG').
        environment: The deployment environment (e.g., 'development', 'production').
    """

    class CustomJsonFormatter(formatter.JsonFormatter):
        """
        Custom log formatter to add standard fields to every log record.
        """

        def add_fields(self, log_record, record, message_dict):
            super().add_fields(log_record, record, message_dict)
            # Use UTC time for consistency
            log_record["timestamp"] = datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
            log_record["level"] = record.levelname.upper()
            log_record["message"] = record.getMessage()
            # Add context from the setup call
            log_record["service"] = service_name
            log_record["env"] = environment
            # Add correlation ID from context var
            log_record["correlation_id"] = get_correlation_id()

            # Clean up redundant fields from the base class
            if "asctime" in log_record:
                del log_record["asctime"]
            if "levelname" in log_record:
                del log_record["levelname"]
            if "exc_info" in log_record and record.exc_info:
                log_record["exc_info"] = self.formatException(record.exc_info)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())

    # Create a handler for console output (stdout)
    log_handler = logging.StreamHandler(sys.stdout)

    # Set the custom JSON formatter
    formatter_instance = CustomJsonFormatter()
    log_handler.setFormatter(formatter_instance)

    # Clear existing handlers and add the new one to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(log_handler)

    # Mute noisy loggers from third-party libraries if needed
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.error").disabled = True


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance for a specific module.

    Assumes `setup_logging` has already been called.

    Args:
        name: The name of the logger, typically `__name__`.

    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)