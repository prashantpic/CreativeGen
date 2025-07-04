from pydantic import PostgresDsn, HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized, type-safe configuration management for the application.
    Loads configuration from environment variables.
    """
    # Project Settings
    PROJECT_NAME: str = "CreativeFlow API Platform"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: PostgresDsn

    # RabbitMQ Configuration
    RABBITMQ_URL: str
    WEBHOOK_EXCHANGE_NAME: str = "webhook_events"
    WEBHOOK_DISPATCH_QUEUE_NAME: str = "webhook_dispatch"

    # Downstream Service URLs
    AIGEN_ORCH_SERVICE_URL: HttpUrl
    ODOO_BUSINESS_SERVICE_URL: HttpUrl

    # Security
    SECRET_KEY: str  # Used for signing internal JWTs, etc.

    # CORS Configuration
    ALLOWED_CORS_ORIGINS: list[str] = ["*"]

    # Model configuration for pydantic-settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Instantiate a single settings object for use throughout the application
settings = Settings()