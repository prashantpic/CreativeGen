import os
from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    # Main Application Settings
    PROJECT_NAME: str = "CreativeFlow AI Generation Orchestration Service"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Database Configuration (PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/aigen_db"

    # RabbitMQ Configuration
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_GENERATION_EXCHANGE: str = "generation_jobs_exchange"
    RABBITMQ_N8N_JOB_QUEUE: str = "n8n_generation_jobs"
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = "n8n.job.create"

    # External Service URLs & Callbacks
    N8N_CALLBACK_BASE_URL: AnyHttpUrl = "http://localhost:8000"
    N8N_CALLBACK_SECRET: str = "a-very-secret-key-for-n8n-callbacks"
    CREDIT_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8001/api/v1/credits"
    NOTIFICATION_SERVICE_API_URL: AnyHttpUrl = "http://localhost:8002/api/v1/notifications"

    # Odoo Configuration
    ODOO_URL: AnyHttpUrl = "http://localhost:8069"
    ODOO_DB: str = "odoo"
    ODOO_UID: int = 1
    ODOO_PASSWORD: str = "admin"

    # Feature Toggles
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = False
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = True
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = True
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        # To load from a .env file, you'd add:
        # env_file = ".env" 
        # env_file_encoding = 'utf-8'

settings = Settings()