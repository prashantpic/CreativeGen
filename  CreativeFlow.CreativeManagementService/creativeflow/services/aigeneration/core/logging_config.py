import logging
import sys
from pythonjsonlogger import jsonlogger

from .config import settings

def setup_logging():
    """
    Configures the application's logging.
    Supports structured JSON logging for better parsing in log aggregation systems.
    """
    log_level = settings.LOG_LEVEL.upper()
    
    # Remove any existing handlers
    # This is important if this function is called multiple times, e.g., in tests
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if settings.LOG_FORMAT.lower() == "json":
        # Use a handler that outputs JSON
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)
    else:
        # Use a standard text-based handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

    # Configure the root logger
    logging.basicConfig(level=log_level, handlers=[handler])

    # Set log levels for third-party libraries that are too verbose
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("pika").setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level {log_level} and format {settings.LOG_FORMAT}")