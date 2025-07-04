"""
Configuration for application logging.
"""
import logging
import sys

from pythonjsonlogger import jsonlogger

from creativeflow.mlops_service.core.config import get_settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON log formatter.

    Adds service name and other default fields to every log record.
    """
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        if not log_record.get('service'):
            log_record['service'] = 'mlops-service'


def setup_logging(log_level: str = "INFO"):
    """
    Configures structured JSON logging for the MLOps service.

    This function sets up the root logger to output logs in JSON format,
    which is ideal for consumption by log management systems like ELK or Splunk.

    Args:
        log_level: The minimum log level to output (e.g., 'INFO', 'DEBUG').
    """
    logger = logging.getLogger()
    
    # Avoid adding duplicate handlers if this function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(log_level)

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # Configure uvicorn loggers to use our handler
    logging.getLogger("uvicorn.access").handlers = [logHandler]
    logging.getLogger("uvicorn.error").handlers = [logHandler]

    logging.info(f"Logging configured with level: {log_level}")