import logging
import sys
from pythonjsonlogger import jsonlogger

from creativeflow.services.aigeneration.core.config import settings

def setup_logging():
    """
    Configures the application's logging based on environment settings.
    Supports both standard text logging and structured JSON logging.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_format = settings.LOG_FORMAT.lower()

    # Get the root logger
    logger = logging.getLogger("creativeflow")
    logger.setLevel(log_level)

    # Prevent duplicate logs in Uvicorn
    logger.propagate = False

    # Remove existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a handler (console)
    handler = logging.StreamHandler(sys.stdout)

    # Set the formatter
    if log_format == "json":
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Configure logging for key libraries
    logging.getLogger("uvicorn.error").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING) # Can be noisy
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING) # Set to INFO for query debugging
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger.info(f"Logging configured with level={log_level} and format={log_format}")