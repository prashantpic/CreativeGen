import logging
import sys
from pythonjsonlogger import jsonlogger
from creativeflow.services.aigeneration.core.config import settings

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        if not log_record.get('timestamp'):
            log_record['timestamp'] = self.formatTime(record, self.datefmt)

def setup_logging():
    """
    Configures the root logger for the application.
    - Sets the log level from settings.
    - Configures either a JSON or a text-based formatter based on settings.
    - Outputs logs to stdout.
    """
    log_level = settings.LOG_LEVEL.upper()
    
    # Get the root logger
    logger = logging.getLogger("creativeflow")
    logger.setLevel(log_level)
    
    # Prevent duplicate logs in some environments (like uvicorn)
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.LOG_FORMAT.lower() == "json":
        # Format for structured JSON logging
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
        # Format for plain text logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Configure uvicorn loggers to use our handler if present
    # This centralizes log format and output
    logging.getLogger("uvicorn").handlers = [handler]
    logging.getLogger("uvicorn.access").handlers = [handler]

    logger.info(f"Logging configured with level {log_level} and format '{settings.LOG_FORMAT}'")