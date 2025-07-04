"""
Initializes the 'logging' submodule.
Exports the primary logging configuration function, logger getter,
correlation ID utilities, and web framework middleware.

Requirement Mapping: DEP-005 (Standardized Log Format)
"""
from .config import add_correlation_id, get_correlation_id, get_logger, setup_logging
from .middleware import FastAPILoggingMiddleware

__all__ = [
    "setup_logging",
    "get_logger",
    "add_correlation_id",
    "get_correlation_id",
    "FastAPILoggingMiddleware",
]