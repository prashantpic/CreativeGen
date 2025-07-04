"""
Handles application configuration settings.

This module uses Pydantic's BaseSettings to load configuration from environment
variables or a .env file, providing typed and validated settings for the application.
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    """
    Defines the application's configuration settings.
    """
    # Application settings
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # Database configuration
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # MinIO (S3-compatible) Object Storage configuration
    MINIO_ENDPOINT: str = Field(..., env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: SecretStr = Field(..., env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: SecretStr = Field(..., env="MINIO_SECRET_KEY")
    MINIO_USE_SSL: bool = Field(default=False, env="MINIO_USE_SSL")
    MINIO_MODEL_BUCKET_NAME: str = Field(default="ml-models", env="MINIO_MODEL_BUCKET_NAME")
    MINIO_VALIDATION_REPORTS_BUCKET_NAME: str = Field(default="ml-validation-reports", env="MINIO_VALIDATION_REPORTS_BUCKET_NAME")

    # Kubernetes configuration
    KUBERNETES_CONFIG_PATH: Optional[str] = Field(default=None, env="KUBERNETES_CONFIG_PATH")
    KUBERNETES_NAMESPACE_MODELS: str = Field(default="ml-models", env="KUBERNETES_NAMESPACE_MODELS")

    # Security Scanners configuration
    SECURITY_SCANNER_API_ENDPOINT: Optional[str] = Field(default=None, env="SECURITY_SCANNER_API_ENDPOINT")
    SECURITY_SCANNER_API_KEY: Optional[SecretStr] = Field(default=None, env="SECURITY_SCANNER_API_KEY")

    # Optional MLflow integration
    MLFLOW_TRACKING_URI: Optional[str] = Field(default=None, env="MLFLOW_TRACKING_URI")

    # Internal API Key for service-to-service authentication
    INTERNAL_API_KEY: SecretStr = Field(..., env="INTERNAL_API_KEY")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Returns the cached Settings instance.

    Using lru_cache ensures the settings are loaded only once.

    Returns:
        Settings: The application configuration settings object.
    """
    return Settings()