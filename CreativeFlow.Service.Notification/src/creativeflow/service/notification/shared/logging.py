import logging
import sys
from python_json_logger import formatter

def setup_logging(log_level: str):
    """
    Configures structured (JSON) logging for the application.

    This function sets up the root logger to output logs in a machine-readable
    JSON format. This is essential for effective log aggregation, searching,
    and monitoring in a production environment (e.g., using ELK, Loki, or Datadog).

    Args:
        log_level: The minimum log level to capture (e.g., "INFO", "DEBUG").
    """
    logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(log_level.upper())

    # Create a handler to output logs to standard output
    log_handler = logging.StreamHandler(sys.stdout)

    # Use a JSON formatter
    # Including standard log record attributes for comprehensive logs.
    formatter_str = "%(timestamp)s %(levelname)s %(name)s %(message)s"
    json_formatter = formatter.JSONFormatter(formatter_str)

    log_handler.setFormatter(json_formatter)
    logger.addHandler(log_handler)
    
    # Also redirect uvicorn's access logs to our handler
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.handlers = [log_handler]
    uvicorn_logger.propagate = False # Prevent uvicorn from adding its own default handler

    logging.info(f"Logging configured with level: {log_level}")