"""
Provides utilities for reporting exceptions to external error tracking services (e.g., Sentry).
This is a shared component to ensure consistent error reporting.
"""

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def init_error_tracking(
    dsn: str,
    environment: str,
    release_version: str,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.1,
) -> None:
    """
    Initializes the Sentry SDK for error and performance tracking.

    Args:
        dsn: The Sentry DSN for the project.
        environment: The application environment (e.g., 'development', 'production').
        release_version: The current version of the application.
        traces_sample_rate: The percentage of transactions to capture for performance.
        profiles_sample_rate: The percentage of transactions to capture for profiling.
    """
    sentry_logging = LoggingIntegration(
        level=sentry_sdk.logging.INFO,  # Capture info and above as breadcrumbs
        event_level=sentry_sdk.logging.ERROR,  # Send errors as events
    )
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release_version,
        integrations=[sentry_logging],
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
    )


def report_exception(exc: Exception, context: dict | None = None) -> None:
    """
    Captures and sends an exception to the configured error tracking service.

    Args:
        exc: The exception object to report.
        context: An optional dictionary of extra context to add to the report.
    """
    if context:
        with sentry_sdk.push_scope() as scope:
            for key, value in context.items():
                scope.set_extra(key, value)
            sentry_sdk.capture_exception(exc)
    else:
        sentry_sdk.capture_exception(exc)