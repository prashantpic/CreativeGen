import logging
import logging.config
import sys

from .config import get_settings


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configures structured logging for the application.

    This setup uses python-json-logger to format logs as JSON, which is
    ideal for consumption by log management systems. It configures a single
    handler to output logs to stdout.

    Args:
        log_level: The minimum log level to output, e.g., "INFO", "DEBUG".
    """
    settings = get_settings()
    log_level = settings.LOG_LEVEL.upper()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(process)d %(thread)d %(levelname)s %(message)s %(module)s %(funcName)s %(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "json",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["console"], "level": log_level, "propagate": False},
            "uvicorn.error": {"level": log_level},
            "uvicorn.access": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "sqlalchemy.engine": {"handlers": ["console"], "level": "WARNING"},
            "aio_pika": {"handlers": ["console"], "level": "WARNING"},
        },
        "root": {"handlers": ["console"], "level": log_level},
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully with level %s.", log_level)