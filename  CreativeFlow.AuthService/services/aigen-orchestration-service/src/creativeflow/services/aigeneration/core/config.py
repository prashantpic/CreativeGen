import os
from pydantic import BaseSettings, AnyUrl
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    # --- Application Settings ---
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"

    # --- Database ---
    DATABASE_URL: AnyUrl = "postgresql+asyncpg://postgres:password@localhost:5432/aigen_orchestration_db"

    # --- RabbitMQ ---
    RABBITMQ_URL: AnyUrl = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # --- Callbacks & External Services ---
    N8N_CALLBACK_BASE_URL: AnyUrl = "http://localhost:8000"
    N8N_CALLBACK_SHARED_SECRET: str = "a-very-secret-key-for-n8n-callbacks"
    CREDIT_SERVICE_API_URL: AnyUrl = "http://localhost:8001/api/v1"
    NOTIFICATION_SERVICE_API_URL: AnyUrl = "http://localhost:8002/api/v1"

    # --- Odoo (if used directly) ---
    ODOO_URL: AnyUrl = "http://localhost:8069"
    ODOO_DB: str = "odoo"
    ODOO_UID: int = 1
    ODOO_PASSWORD: str = "admin"

    # --- Feature Toggles ---
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True

    class Config:
        case_sensitive = True
        # Load from .env file if it exists
        env_file = os.path.expanduser("~/.env"), ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.
    """
    return Settings()

settings = get_settings()