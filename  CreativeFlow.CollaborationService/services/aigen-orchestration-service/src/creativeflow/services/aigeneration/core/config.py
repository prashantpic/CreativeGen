import os
from pydantic import BaseSettings, AnyUrl
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """
    # Application Settings
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"
    N8N_CALLBACK_SECRET: str = "a_very_secret_key_for_n8n_to_use"
    N8N_CALLBACK_BASE_URL: AnyUrl = "http://localhost:8000"

    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/aigen_orchestration_db"

    # RabbitMQ Configuration
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # External Service URLs
    CREDIT_SERVICE_API_URL: AnyUrl = "http://localhost:8001/api/v1/credits"
    NOTIFICATION_SERVICE_API_URL: AnyUrl = "http://localhost:8002/api/v1/notifications"

    # Odoo Configuration
    ODOO_URL: AnyUrl = "http://localhost:8069"
    ODOO_DB: str = "odoo_db_name"
    ODOO_UID: int = 1
    ODOO_PASSWORD: str = "admin"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json" # "json" or "text"

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True


    class Config:
        # This tells Pydantic to load settings from a .env file if it exists
        env_file = ".env"
        # Pydantic settings are case-insensitive
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings object.
    Using lru_cache ensures the settings are loaded only once.
    """
    return Settings()

settings = get_settings()