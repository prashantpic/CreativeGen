"""
Manages application configuration using Pydantic's BaseSettings.
Loads settings from environment variables for database connections, RabbitMQ details,
and other external service credentials.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines and loads all external configurations and environment variables for the service.
    Pydantic automatically reads values from environment variables, ensuring that
    all required configurations are present at startup.
    """
    # Database Configuration
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10

    # RabbitMQ Messaging Configuration
    RABBITMQ_URL: str
    GENERATION_JOB_QUEUE: str = "creativeflow.jobs.generation"

    # Security Configuration
    N8N_CALLBACK_SECRET: str | None = None

    # External Service URLs
    ODOO_SERVICE_URL: str
    NOTIFICATION_SERVICE_URL: str

    # Pydantic model configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Create a singleton instance of the settings to be used throughout the application
settings = Settings()