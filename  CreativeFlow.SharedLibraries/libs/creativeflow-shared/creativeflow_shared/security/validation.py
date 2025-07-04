"""
Provides common validation utilities, including wrappers for Pydantic
and specific security checks for things like password strength.
"""
import re
import uuid

import pydantic

from ..core.constants import MIN_PASSWORD_LENGTH
from ..datamodels.common import ErrorDetailDTO
from ..error_handling.exceptions import ValidationError as SharedValidationError


def validate_request_payload(
    payload: dict, schema: type[pydantic.BaseModel]
) -> pydantic.BaseModel:
    """
    Validates a dictionary payload against a Pydantic schema.

    If validation fails, it catches the Pydantic error and re-raises it
    as a standardized `SharedValidationError`, converting the error details
    into the application's `ErrorDetailDTO` format.

    Args:
        payload: The input dictionary to validate.
        schema: The Pydantic model class to validate against.

    Returns:
        A validated instance of the Pydantic model.

    Raises:
        SharedValidationError: If the payload fails validation.
    """
    try:
        return schema.model_validate(payload)
    except pydantic.ValidationError as e:
        error_details = [
            ErrorDetailDTO(
                field=str(err["loc"][0]) if err["loc"] else "payload",
                message=err["msg"],
                code=err.get("type"),
            )
            for err in e.errors()
        ]
        raise SharedValidationError(details=error_details) from e


def is_strong_password(
    password: str,
    min_length: int = MIN_PASSWORD_LENGTH,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digit: bool = True,
    require_special_char: bool = True,
) -> bool:
    """
    Checks if a password meets specified complexity criteria.

    Args:
        password: The password string to check.
        min_length: The minimum required length.
        require_uppercase: Whether an uppercase letter is required.
        require_lowercase: Whether a lowercase letter is required.
        require_digit: Whether a digit is required.
        require_special_char: Whether a special character is required.

    Returns:
        True if the password is strong, False otherwise.
    """
    if len(password) < min_length:
        return False
    if require_uppercase and not re.search(r"[A-Z]", password):
        return False
    if require_lowercase and not re.search(r"[a-z]", password):
        return False
    if require_digit and not re.search(r"\d", password):
        return False
    if require_special_char and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Checks if a string is a valid UUID.

    Args:
        uuid_string: The string to validate.

    Returns:
        True if the string is a valid UUID, False otherwise.
    """
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError, AttributeError):
        return False