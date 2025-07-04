"""
Initializes the security scanners infrastructure package.

This package provides adapters for interacting with various security scanning
tools (e.g., Snyk, Clair), abstracting their specific APIs or CLIs from the
core validation logic of the service.
"""
from .scanner_adapter import ScannerAdapter

__all__ = ["ScannerAdapter"]