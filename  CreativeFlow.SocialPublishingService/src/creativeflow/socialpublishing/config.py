"""
Configuration settings for the service, loaded from environment variables
or .env files using Pydantic BaseSettings.
"""
import functools
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Defines and loads application settings from the environment.
    """
    # --- Core Service Dependencies ---
    DATABASE_URL: str
    AES_KEY: str  # Must be 32 bytes, base64 encoded

    # --- External Social Media Platform APIs ---
    INSTAGRAM_APP_ID: str
    INSTAGRAM_APP_SECRET: str
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET: str
    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    TWITTER_API_KEY: str
    TWITTER_API_SECRET_KEY: str
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    PINTEREST_APP_ID: str
    PINTEREST_APP_SECRET: str
    TIKTOK_CLIENT_KEY: Optional[str] = None
    TIKTOK_CLIENT_SECRET: Optional[str] = None

    # --- Internal Service Communication ---
    AUTH_SERVICE_URL: str
    SERVICE_BASE_URL: str  # The base URL of this service itself

    # --- Operational Settings ---
    LOG_LEVEL: str = "INFO"
    REDIS_URL: Optional[str] = None
    INSIGHTS_CACHE_TTL_SECONDS: int = 3600

    # --- API Client Retry Strategy ---
    MAX_API_RETRIES: int = 3
    API_RETRY_DELAY_SECONDS: float = 1.0
    API_RETRY_BACKOFF_FACTOR: float = 2.0

    class Config:
        """
        Pydantic settings configuration.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@functools.lru_cache
def get_settings() -> Settings:
    """
    Get the application settings.

    Uses lru_cache to load the settings only once.

    Returns:
        An instance of the Settings class.
    """
    return Settings()