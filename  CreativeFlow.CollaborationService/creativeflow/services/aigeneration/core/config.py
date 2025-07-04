from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    # --- Project Settings ---
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"

    # --- Database Configuration ---
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@host:port/dbname"

    # --- RabbitMQ Configuration ---
    RABBITMQ_URL: str = "amqp://user:pass@host:port/vhost"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # --- External Service URLs & Callbacks ---
    N8N_CALLBACK_BASE_URL: AnyHttpUrl = "http://localhost:8000"
    CREDIT_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8001/api/v1/credits"
    NOTIFICATION_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8002/api/v1/notifications"

    # --- Odoo Configuration ---
    ODOO_URL: Optional[AnyHttpUrl]
    ODOO_DB: Optional[str]
    ODOO_UID: Optional[int]
    ODOO_PASSWORD: Optional[str]

    # --- Logging Configuration ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"

    # --- Security ---
    N8N_CALLBACK_SECRET: str = "change-me-in-production"

    # --- Feature Toggles ---
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True

    class Config:
        # This allows Pydantic to read variables from a .env file
        env_file = ".env"
        case_sensitive = True


# Create a single instance of the settings to be used throughout the application
settings = Settings()