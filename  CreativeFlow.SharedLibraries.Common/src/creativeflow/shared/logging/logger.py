"""
Provides a utility to obtain a pre-configured logger instance.
"""
import logging


def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a logger instance with the specified name.

    It is assumed that setup_logging() has already been called at application
    startup to configure the root logger. This function simply provides a
    convenient way to get a named logger that will inherit the root
    configuration.

    Args:
        name: The name for the logger, typically the `__name__` of the calling
              module.

    Returns:
        A pre-configured logger instance.
    """
    return logging.getLogger(name)