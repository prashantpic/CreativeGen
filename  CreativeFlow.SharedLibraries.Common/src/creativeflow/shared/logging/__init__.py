"""
Initializes the logging sub-package, providing standardized logging setup and access.
"""
from .config import setup_logging
from .logger import get_logger

__all__ = [
    "setup_logging",
    "get_logger",
]