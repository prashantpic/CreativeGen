import logging
import sys
import json
from loguru import logger as loguru_logger

from creativeflow.services.aigeneration.core.config import settings

class InterceptHandler(logging.Handler):
    """
    Handler to intercept standard logging messages and redirect them to Loguru.
    """
    def emit(self, record: logging.LogRecord):
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    """
    Configures the application's logging using Loguru.
    - Intercepts standard logging.
    - Sets level from environment settings.
    - Configures JSON or text format based on environment settings.
    """
    # Intercept everything from the standard logger
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Remove default handler and add a new one with configured format
    loguru_logger.remove()
    
    # Configure format based on settings
    if settings.LOG_FORMAT.lower() == "json":
        loguru_logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL.upper(),
            format="{message}",
            serialize=True,
            enqueue=True, # Make logging async
            backtrace=False, # Avoid large stack traces in JSON logs for production
            diagnose=settings.LOG_LEVEL.upper() == "DEBUG"
        )
    else:
        loguru_logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL.upper(),
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

    loguru_logger.info(f"Logging configured with level={settings.LOG_LEVEL} and format={settings.LOG_FORMAT}")