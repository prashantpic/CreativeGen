"""
Handles application configuration using Pydantic's BaseSettings for loading
from environment variables or .env files.
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines application settings, loaded from environment variables or a .env file.

    Attributes:
        DATABASE_URL: The connection string for the PostgreSQL database.
        AUTH_SERVICE_URL: The URL for the authentication service (if needed).
        LOG_LEVEL: The logging level for the application.
        ENVIRONMENT: The runtime environment (e.g., 'development', 'production').
        API_V1_STR: The prefix for version 1 of the API.
        PROJECT_NAME: The name of the project.
    """
    DATABASE_URL: str
    AUTH_SERVICE_URL: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "UserProfile Service"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.

    Using lru_cache ensures that the settings are loaded only once, improving
    performance by avoiding repeated file I/O or environment variable reads.

    Returns:
        An instance of the Settings class.
    """
    return Settings()