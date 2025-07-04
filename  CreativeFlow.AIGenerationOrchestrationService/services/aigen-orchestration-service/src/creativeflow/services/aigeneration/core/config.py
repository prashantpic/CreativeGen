from typing import Optional
from pydantic import BaseSettings, Field, PostgresDsn, AmqpDsn, AnyHttpUrl


class Settings(BaseSettings):
    """
    Application configuration settings, loaded from environment variables or a .env file.
    """

    # --- Key Configuration Variables ---
    PROJECT_NAME: str = Field(
        "CreativeFlow AI Generation Orchestration Service",
        description="Name of the project."
    )
    API_V1_STR: str = Field("/api/v1", description="API prefix for version 1.")

    # Database Configuration
    DATABASE_URL: PostgresDsn = Field(
        "postgresql+asyncpg://user:pass@localhost:5432/aigen_orchestration_db",
        description="Connection string for the PostgreSQL database."
    )

    # RabbitMQ Configuration
    RABBITMQ_URL: AmqpDsn = Field(
        "amqp://user:pass@localhost:5672/",
        description="Connection string for RabbitMQ."
    )
    RABBITMQ_GENERATION_EXCHANGE: str = Field(
        "generation_jobs_exchange",
        description="Name of the RabbitMQ exchange for generation jobs."
    )
    RABBITMQ_N8N_JOB_QUEUE: str = Field(
        "n8n_generation_jobs",
        description="Name of the RabbitMQ queue n8n consumes from."
    )
    RABBITMQ_N8N_JOB_ROUTING_KEY: str = Field(
        "n8n.job.generation",
        description="Routing key for n8n generation jobs."
    )

    # External Services and Callbacks
    N8N_CALLBACK_BASE_URL: AnyHttpUrl = Field(
        "http://localhost:8000",
        description="Base URL for this service that n8n will use for callbacks."
    )
    CREDIT_SERVICE_API_URL: AnyHttpUrl = Field(
        "http://localhost:8001/api/v1/credits",
        description="Base URL for the Credit/Subscription Service API."
    )
    NOTIFICATION_SERVICE_API_URL: AnyHttpUrl = Field(
        "http://localhost:8002/api/v1/notifications",
        description="Base URL for the Notification Service API."
    )
    N8N_CALLBACK_SHARED_SECRET: Optional[str] = Field(
        None,
        description="A shared secret key to validate incoming callbacks from n8n."
    )


    # Odoo Configuration
    ODOO_URL: Optional[AnyHttpUrl] = Field(None, description="URL for the Odoo XML-RPC/JSON-RPC endpoint.")
    ODOO_DB: Optional[str] = Field(None, description="Odoo database name.")
    ODOO_UID: Optional[int] = Field(None, description="Odoo user ID for API access.")
    ODOO_PASSWORD: Optional[str] = Field(None, description="Odoo password for API access.")

    # Logging Configuration
    LOG_LEVEL: str = Field("INFO", description='Logging level (e.g., "INFO", "DEBUG").')
    LOG_FORMAT: str = Field("json", description='Log format (e.g., "json", "text").')

    # --- Feature Toggles ---
    ENABLE_ADVANCED_MODEL_SELECTOR: bool = Field(
        False,
        description="If true, enables logic for more complex AI model selection."
    )
    ENABLE_DETAILED_N8N_ERROR_LOGGING: bool = Field(
        True,
        description="If true, logs more verbose error details from n8n callbacks."
    )
    ENABLE_CREDIT_REFUND_ON_SYSTEM_FAILURE: bool = Field(
        True,
        description="If true, automatically triggers credit refund attempts for system-caused generation failures."
    )

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()