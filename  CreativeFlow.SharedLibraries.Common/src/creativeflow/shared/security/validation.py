"""
Provides input validation utilities, leveraging Pydantic models.
"""
import re
import uuid
from typing import Any, Type

from pydantic import ValidationError as PydanticValidationError

from ..constants.general import EMAIL_REGEX, UUID_REGEX
from ..dtos.base_dto import BaseDTO
from ..exceptions.domain_exceptions import ValidationError


def validate_payload(payload: Any, model_cls: Type[BaseDTO]) -> BaseDTO:
    """
    Validates a payload against a given Pydantic model.

    Args:
        payload: The data to validate (e.g., a dictionary from a request).
        model_cls: The Pydantic model class to validate against.

    Returns:
        An instance of `model_cls` if validation is successful.

    Raises:
        ValidationError: If the payload fails Pydantic validation. The
                         `details` attribute will contain structured error
                         information from Pydantic.
    """
    try:
        return model_cls.model_validate(payload)
    except PydanticValidationError as e:
        error_details = e.errors()
        raise ValidationError(
            message="Payload validation failed.", details=error_details
        ) from e


def is_valid_email(email_string: str) -> bool:
    """
    Checks if a string is a validly formatted email address.

    Args:
        email_string: The string to validate.

    Returns:
        True if the string is a valid email format, False otherwise.
    """
    if not isinstance(email_string, str):
        return False
    return bool(re.fullmatch(EMAIL_REGEX, email_string))


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Checks if a string is a validly formatted UUID.

    This performs a quick regex check for format and then a stricter check
    by attempting to parse it into a UUID object.

    Args:
        uuid_string: The string to validate.

    Returns:
        True if the string is a valid UUID, False otherwise.
    """
    if not isinstance(uuid_string, str):
        return False

    # Regex check is faster for rejecting obviously wrong formats
    if not re.fullmatch(UUID_REGEX, uuid_string):
        return False

    # Stricter check to ensure it's a valid UUID value
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False