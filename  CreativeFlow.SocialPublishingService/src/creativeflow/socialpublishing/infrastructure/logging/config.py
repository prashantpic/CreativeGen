"""
Configuration for structured logging.
"""
import logging
import sys

from pythonjsonlogger import jsonlogger


def setup_logging(log_level_str: str = "INFO"):
    """
    Configures structured (JSON) logging for the application.

    This setup ensures that logs are emitted in a machine-readable format,
    which is beneficial for log aggregation and analysis systems.

    Args:
        log_level_str: The desired logging level as a string (e.g., "INFO", "DEBUG").
    """
    logger = logging.getLogger("creativeflow.socialpublishing")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Prevent logs from propagating to the root logger, which might have
    # a different format.
    logger.propagate = False

    # Use a stream handler to output to stderr
    log_handler = logging.StreamHandler(sys.stdout)

    # Use JsonFormatter for structured logs
    formatter = jsonlogger.JsonFormatter(
        fmt=(
            "%(asctime)s %(levelname)s %(name)s %(module)s "
            "%(funcName)s %(lineno)d %(message)s"
        )
    )
    log_handler.setFormatter(formatter)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.addHandler(log_handler)

    # Optionally, configure uvicorn's access logger to be JSON as well
    # This provides consistency in log formats across the application.
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = [log_handler]
    uvicorn_access_logger.propagate = False