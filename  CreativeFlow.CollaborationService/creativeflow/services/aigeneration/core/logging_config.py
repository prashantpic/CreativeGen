import logging
import sys
from pythonjsonlogger import jsonlogger

from creativeflow.services.aigeneration.core.config import settings

def setup_logging():
    """
    Configures the application's logging based on settings.
    Supports both standard text and structured JSON logging.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_format = settings.LOG_FORMAT.lower()

    if log_format == "json":
        # Use a custom formatter for structured JSON logs
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
        )
    else:
        # Use a standard text formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    # Get the root logger
    logger = logging.getLogger()
    
    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a handler to output to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    # Add the handler to the root logger
    logger.addHandler(handler)
    
    # Set the log level for the root logger
    logger.setLevel(log_level)

    # Set log levels for third-party libraries to avoid excessive verbosity
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)
    
    # Log the initial configuration
    logging.info(
        "Logging configured with level=%s and format=%s", log_level, log_format
    )