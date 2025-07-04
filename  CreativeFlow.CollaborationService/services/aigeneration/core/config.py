import os
from pydantic import BaseSettings, AnyUrl
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or a .env file.
    """
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: AnyUrl

    # RabbitMQ
    RABBITMQ_URL: AnyUrl
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # External Services & Callbacks
    N8N_CALLBACK_BASE_URL: AnyUrl
    CREDIT_SERVICE_API_URL: AnyUrl
    NOTIFICATION_SERVICE_API_URL: AnyUrl

    # Odoo (if used)
    ODOO_URL: Optional[AnyUrl]
    ODOO_DB: Optional[str]
    ODOO_UID: Optional[int]
    ODOO_PASSWORD: Optional[str]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"

    # Security
    N8N_CALLBACK_SECRET: str

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True

    class Config:
        case_sensitive = True
        # Load from .env file if it exists
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instantiate settings
settings = Settings()