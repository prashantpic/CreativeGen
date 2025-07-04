"""
Defines general, application-wide constants used across multiple services.
"""

# A robust regex for email validation based on common standards.
EMAIL_REGEX: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# A standard regex for UUID format validation.
UUID_REGEX: str = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

# Default timeout in seconds for external service requests.
DEFAULT_REQUEST_TIMEOUT_SECONDS: int = 30

# Maximum character length for user-provided full names.
MAX_FULL_NAME_LENGTH: int = 100

# Maximum character length for usernames.
MAX_USERNAME_LENGTH: int = 50