```python
import logging
import logging.config
import sys


def setup_logging(log_level: str = "INFO"):
    """
    Configures structured logging for the application.

    Args:
        log_level: The minimum log level to output (e.g., "INFO", "DEBUG").
    """
    # For production, consider using a library like python-json-logger
    # to output logs in a machine-readable JSON format.
    # formatter = "json"
    formatter = "default"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": "%(levelname)-8s | %(asctime)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            # Example JSON formatter configuration
            # "json": {
            #     "()": "python_json_logger.jsonlogger.JsonFormatter",
            #     "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s"
            # }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": formatter,
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
            "sqlalchemy.engine": {"handlers": ["console"], "level": "WARNING", "propagate": False},
            "alembic": {"handlers": ["console"], "level": "INFO", "propagate": False},
            "httpx": {"handlers": ["console"], "level": "WARNING", "propagate": False},
            "aio_pika": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        },
        "root": {
            "handlers": ["console"],
            "level": log_level.upper(),
        },
    }

    logging.config.dictConfig(logging_config)
    logging.info(f"Logging configured with level {log_level.upper()}")
```