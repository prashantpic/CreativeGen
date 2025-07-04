import logging
import sys
from pythonjsonlogger import jsonlogger
from creativeflow.services.aigeneration.core.config import settings

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.created
        if not log_record.get('level'):
            log_record['level'] = record.levelname.upper()
        else:
            log_record['level'] = log_record['level'].upper()
        
        # Add correlation ID if available (needs to be set in a context var by a middleware)
        # from contextvars import ContextVar
        # correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default=None)
        # correlation_id = correlation_id_var.get()
        # if correlation_id:
        #     log_record['correlation_id'] = correlation_id

def setup_logging():
    """
    Configures the logging for the application.
    Supports both standard text and structured JSON formats.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_format = settings.LOG_FORMAT.lower()

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create a new handler (console)
    handler = logging.StreamHandler(sys.stdout)

    if log_format == "json":
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Configure logging for key libraries
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    # Initial log message
    logging.getLogger(__name__).info(f"Logging configured with level={log_level} and format={log_format}")