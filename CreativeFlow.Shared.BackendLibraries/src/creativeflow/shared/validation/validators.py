"""
This module contains common, reusable Pydantic field validators for standard
data validation tasks like password complexity or username formatting. These can
be imported and used directly in DTO definitions across multiple services.
"""
import re


def validate_password_complexity(password: str) -> str:
    """
    Pydantic-compatible validator to enforce password complexity rules.

    Rules:
    - At least 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character from the set @$!%*?&

    Args:
        password: The password string to validate.

    Raises:
        ValueError: If the password does not meet the complexity requirements.

    Returns:
        The original password string if validation passes.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    # Regex to enforce all rules simultaneously
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$"
    if not re.match(pattern, password):
        raise ValueError(
            "Password must be at least 12 characters and contain at least one uppercase letter, "
            "one lowercase letter, one number, and one special character (@$!%*?&)."
        )
    return password


def validate_username_format(username: str) -> str:
    """
    Pydantic-compatible validator to enforce username format rules.

    Rules:
    - 3 to 50 characters in length
    - Can only contain alphanumeric characters (a-z, A-Z, 0-9) and underscores (_)

    Args:
        username: The username string to validate.

    Raises:
        ValueError: If the username does not meet the format requirements.

    Returns:
        The original username string if validation passes.
    """
    if not isinstance(username, str):
        raise TypeError("Username must be a string")

    pattern = r"^[a-zA-Z0-9_]{3,50}$"
    if not re.match(pattern, username):
        raise ValueError(
            "Username must be 3-50 characters long and can only contain "
            "letters, numbers, and underscores."
        )
    return username