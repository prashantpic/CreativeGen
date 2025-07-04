from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or .env file.
    """
    # Application Settings
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Database Configuration (PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/creativeflow_aigen"

    # RabbitMQ Configuration
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # n8n Callback Configuration
    N8N_CALLBACK_BASE_URL: AnyHttpUrl = "http://localhost:8000"
    N8N_CALLBACK_SECRET: str = "a-very-secret-token"

    # External Service URLs
    CREDIT_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8001/api/v1"
    NOTIFICATION_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8002/api/v1"

    # Odoo Configuration
    ODOO_URL: Optional[AnyHttpUrl]
    ODOO_DB: Optional[str]
    ODOO_UID: Optional[int]
    ODOO_PASSWORD: Optional[str]

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()