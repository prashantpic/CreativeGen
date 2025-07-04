"""
Configures structured logging for the application.
"""
import logging
import sys

from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO"):
    """
    Sets up application-wide structured JSON logging.

    This configuration directs logs to stdout, formats them as JSON for
    easier parsing by log aggregation systems, and sets the logging level
    based on the application's configuration.

    Args:
        log_level: The minimum level of logs to output (e.g., "INFO", "DEBUG").
    """
    logger = logging.getLogger()
    
    # Remove any existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    log_handler = logging.StreamHandler(sys.stdout)
    
    # Define the format for structured logs
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s"
    )
    
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    
    # Set the log level from the string value
    log_level_enum = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(log_level_enum)
    
    logging.info(f"Logging configured with level: {log_level}")