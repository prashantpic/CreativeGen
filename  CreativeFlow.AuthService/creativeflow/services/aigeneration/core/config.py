from pydantic import BaseSettings, AnyUrl
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or a .env file.
    """
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: AnyUrl

    # RabbitMQ Configuration
    RABBITMQ_URL: AnyUrl
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.generate"

    # External Service & Callback URLs
    N8N_CALLBACK_BASE_URL: AnyUrl
    CREDIT_SERVICE_API_URL: AnyUrl
    NOTIFICATION_SERVICE_API_URL: AnyUrl
    N8N_CALLBACK_SECRET: str

    # Odoo Configuration
    ODOO_URL: Optional[AnyUrl]
    ODOO_DB: Optional[str]
    ODOO_UID: Optional[int]
    ODOO_PASSWORD: Optional[str]

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json" # "json" or "text"

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()