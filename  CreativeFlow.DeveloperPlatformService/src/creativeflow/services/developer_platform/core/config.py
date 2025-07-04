"""
Handles application configuration loading using Pydantic for settings management
from environment variables or .env files.
"""

from functools import lru_cache
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Defines and loads application settings from environment variables or a .env file.
    """
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dev_platform_db"

    # Messaging Configuration
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_WEBHOOK_EXCHANGE_NAME: str = "webhook_events_exchange"
    RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX: str = "webhook.event"

    # Security Configuration
    JWT_SECRET_KEY: str = "a_very_secret_key_for_user_jwt_validation"
    API_KEY_HEADER_NAME: str = "X-API-KEY"
    WEBHOOK_HMAC_SECRET_KEY: str = "a_global_secret_for_signing_webhook_payloads"

    # External Service URLs
    AI_GENERATION_SERVICE_URL: HttpUrl = "http://localhost:8001/api/v1"
    ASSET_MANAGEMENT_SERVICE_URL: HttpUrl = "http://localhost:8002/api/v1"
    USER_TEAM_SERVICE_URL: HttpUrl = "http://localhost:8003/api/v1"
    AUTH_SERVICE_URL: HttpUrl = "http://localhost:8004/api/v1"
    
    # Cache/Rate Limiting Configuration
    REDIS_URL: str = "redis://localhost:6379/0"

    # Application Behavior
    LOG_LEVEL: str = "INFO"
    DEFAULT_RATE_LIMIT_REQUESTS: int = 100
    DEFAULT_RATE_LIMIT_PERIOD_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    
    Using lru_cache ensures the settings are loaded only once.
    
    Returns:
        Settings: The application settings object.
    """
    return Settings()