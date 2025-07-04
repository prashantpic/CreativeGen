"""
Configures standardized structured JSON logging for the platform.
"""
import logging
import os
from typing import Any, Dict, Optional

from python_json_logger import jsonlogger

_logging_configured = False


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON formatter to add static fields to all log records.
    """
    def __init__(self, *args: Any, static_fields: Optional[Dict[str, Any]] = None, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._static_fields = static_fields or {}

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record.update(self._static_fields)


def setup_logging(
    log_level: str = "INFO",
    service_name: Optional[str] = None,
    environment: Optional[str] = None,
) -> None:
    """
    Configures structured JSON logging for the application.

    This function sets up a JSON formatter for the root logger, ensuring that all
    log messages are output in a machine-readable format suitable for log
    aggregation systems. It can be safely called multiple times, but will only
    perform configuration once.

    Args:
        log_level: The logging level (e.g., 'DEBUG', 'INFO'). Defaults to 'INFO'.
                   Can be overridden by the LOG_LEVEL environment variable.
        service_name: The name of the service.
                      Can be overridden by the SERVICE_NAME environment variable.
        environment: The deployment environment (e.g., 'dev', 'prod').
                     Can be overridden by the ENVIRONMENT environment variable.
    """
    global _logging_configured
    if _logging_configured:
        return

    effective_log_level_str = os.getenv("LOG_LEVEL", log_level).upper()
    effective_log_level = getattr(logging, effective_log_level_str, logging.INFO)

    effective_service_name = os.getenv(
        "SERVICE_NAME", service_name or "creativeflow-service"
    )
    effective_environment = os.getenv("ENVIRONMENT", environment or "development")

    static_fields = {
        "service_name": effective_service_name,
        "environment": effective_environment,
    }

    formatter = CustomJsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
        datefmt="%Y-%m-%dT%H:%M:%S.%fZ",
        static_fields=static_fields
    )

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(log_handler)
    root_logger.setLevel(effective_log_level)

    _logging_configured = True

    # Log that configuration is complete
    # logging.getLogger(__name__).info(
    #     "Logging configured for service '%s' in '%s' at level '%s'",
    #     effective_service_name, effective_environment, effective_log_level_str
    # )