import logging
import sys
from pythonjsonlogger import jsonlogger

from .config import settings

def setup_logging():
    """
    Configures the application's logging based on settings.
    Supports structured JSON logging.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_format = settings.LOG_FORMAT.lower()

    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)

    if log_format == "json":
        # Example format: {"timestamp": "...", "level": "INFO", "name": "...", "message": "..."}
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
    else:
        # Standard text format
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    logger.info(f"Logging configured with level={log_level} and format={log_format}")