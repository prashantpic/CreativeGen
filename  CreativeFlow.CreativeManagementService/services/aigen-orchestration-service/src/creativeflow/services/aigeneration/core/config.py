"""
Handles application configuration using Pydantic Settings.
Loads settings from environment variables or .env files.
"""
from functools import lru_cache
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Project Settings
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str

    # RabbitMQ Configuration
    RABBITMQ_URL: SecretStr
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # n8n Callback Configuration
    N8N_CALLBACK_BASE_URL: str
    N8N_WEBHOOK_SECRET: SecretStr

    # External Service URLs
    CREDIT_SERVICE_API_URL: str
    NOTIFICATION_SERVICE_API_URL: str

    # Odoo Configuration
    ODOO_URL: str
    ODOO_DB: str
    ODOO_UID: int
    ODOO_PASSWORD: SecretStr

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json" # "json" or "text"

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.
    """
    return Settings()