import logging
import sys
import json
from pythonjsonlogger import jsonlogger

from creativeflow.services.aigeneration.core.config import settings

class JsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON log formatter to add standard log attributes.
    """
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.created

def setup_logging():
    """
    Configures the application's logging based on environment settings.
    Supports both plain text and structured JSON logging.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_format = settings.LOG_FORMAT.lower()

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a handler to stream logs to stdout
    handler = logging.StreamHandler(sys.stdout)
    
    if log_format == "json":
        # Use our custom JSON formatter
        formatter = JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
        # Use a standard text formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Configure logging for key libraries
    # Set uvicorn access logs to be handled by our logger
    logging.getLogger("uvicorn.access").handlers = [handler]
    logging.getLogger("uvicorn.error").handlers = [handler]
    # Adjust log levels for noisy libraries
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    # Log initial configuration
    logging.info(f"Logging configured with level={log_level} and format={log_format}")