import logging
import sys
from pythonjsonlogger import jsonlogger
from creativeflow.services.aigeneration.core.config import settings

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON log formatter to add standard attributes.
    """
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['name'] = record.name
        # In a real app, you would extract correlation_id from request context
        # log_record['correlation_id'] = get_correlation_id()

def setup_logging():
    """
    Configures Python's logging module for the application.
    - Sets log level from environment settings.
    - Supports structured JSON logging.
    """
    log_level = settings.LOG_LEVEL.upper()
    
    logger = logging.getLogger("creativeflow.services.aigeneration")
    logger.setLevel(log_level)
    
    # Prevent logs from propagating to the root logger
    logger.propagate = False
    
    handler = logging.StreamHandler(sys.stdout)
    
    if settings.LOG_FORMAT == "json":
        # Example format: %(asctime)s %(name)s %(levelname)s %(message)s
        formatter = CustomJsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
        )
        
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Configure logging for other libraries used
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)