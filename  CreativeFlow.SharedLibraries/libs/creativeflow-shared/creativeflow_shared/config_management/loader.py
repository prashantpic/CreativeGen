"""
Provides utilities for loading configurations from environment variables
and populating Pydantic models for validation and type-safe access.
"""
from typing import Type, TypeVar

from pydantic import ValidationError as PydanticValidationError
from pydantic_settings import BaseSettings

from ..datamodels.common import ErrorDetailDTO
from ..error_handling.exceptions import ValidationError as SharedValidationError

T = TypeVar("T", bound=BaseSettings)


def load_app_config(
    config_schema: Type[T], dotenv_path: str | None = None
) -> T:
    """
    Loads and validates application configuration from environment variables.

    This function uses a Pydantic `BaseSettings` schema to automatically
    read, parse, and validate configuration from the environment. It supports
    loading from a `.env` file for local development.

    Args:
        config_schema: A Pydantic class inheriting from `pydantic_settings.BaseSettings`.
        dotenv_path: Optional path to a `.env` file to load.

    Returns:
        A validated instance of the configuration schema.

    Raises:
        SharedValidationError: If configuration validation fails.
    """
    try:
        settings_kwargs = {}
        if dotenv_path:
            settings_kwargs["_env_file"] = dotenv_path
            settings_kwargs["_env_file_encoding"] = "utf-8"

        return config_schema(**settings_kwargs)

    except PydanticValidationError as e:
        error_details = [
            ErrorDetailDTO(
                field=".".join(map(str, err["loc"])),
                message=err["msg"],
                code=err.get("type"),
            )
            for err in e.errors()
        ]
        raise SharedValidationError(
            message="Application configuration validation failed. Check environment variables.",
            details=error_details,
        ) from e