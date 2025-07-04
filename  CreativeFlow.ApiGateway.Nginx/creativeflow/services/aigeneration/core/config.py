```python
import os
from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """
    # --- Application Configuration ---
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json" # "text" or "json"
    N8N_CALLBACK_SECRET: str = "a_very_secret_key"

    # --- Database Configuration ---
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@host:port/dbname"

    # --- RabbitMQ Configuration ---
    RABBITMQ_URL: str = "amqp://user:pass@host:port/vhost"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # --- External Service URLs ---
    N8N_CALLBACK_BASE_URL: AnyHttpUrl = "http://localhost:8000"
    CREDIT_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8001"
    NOTIFICATION_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8002"

    # --- Odoo Configuration ---
    ODOO_URL: AnyHttpUrl = "http://localhost:8069"
    ODOO_DB: str = "odoo"
    ODOO_UID: int = 1
    ODOO_PASSWORD: str = "admin"

    # --- Feature Toggles ---
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True

    # --- CORS ---
    # Example: "http://localhost,http://localhost:4200,http://localhost:3000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        # Load from .env file if it exists
        env_file = os.path.expanduser("~/.env")
        env_file_encoding = 'utf-8'

settings = Settings()
```