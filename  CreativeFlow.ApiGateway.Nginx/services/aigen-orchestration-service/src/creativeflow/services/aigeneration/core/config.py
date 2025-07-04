from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/aigen_db"

    # RabbitMQ Configuration
    RABBITMQ_URL: str = "amqp://user:pass@localhost:5672/"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # Service URLs
    N8N_CALLBACK_BASE_URL: AnyHttpUrl = "http://localhost:8000"
    N8N_CALLBACK_SECRET: str = "a-very-secret-key-for-n8n-callbacks" # Shared secret for securing callbacks
    CREDIT_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8001/api/v1"
    NOTIFICATION_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8002/api/v1"
    
    # Odoo Configuration
    ODOO_URL: str = "http://localhost:8069"
    ODOO_DB: str = "odoo"
    ODOO_UID: int = 1
    ODOO_PASSWORD: str = "admin"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "text"

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()