"""
Standardized logger configuration for the CreativeFlow Notification Service.

This module provides a centralized function to obtain a configured logger instance,
ensuring consistent log formatting and output across the entire application.
It prevents duplicate handler registrations, making it safe to call from any module.
"""
import logging
import sys


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Configures and retrieves a logger instance.

    This function sets up a logger with a specified name and level,
    outputting to stdout with a standard format. It ensures that handlers
    are not added more than once to the same logger.

    Args:
        name: The name for the logger, typically the module's `__name__`.
        level: The logging level as a string (e.g., "INFO", "DEBUG").

    Returns:
        A configured instance of logging.Logger.
    """
    logger = logging.getLogger(name)
    
    try:
        log_level = logging.getLevelName(level.upper())
        logger.setLevel(log_level)
    except ValueError:
        logger.setLevel(logging.INFO)
        logger.warning(f"Invalid LOG_LEVEL '{level}'. Defaulting to INFO.")

    # Prevent adding duplicate handlers if the function is called multiple times.
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger