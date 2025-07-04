"""
Handles application configuration settings.

This module uses Pydantic's BaseSettings to define and load configuration
from environment variables or a .env file. This provides a single, typed
source of truth for all configuration parameters needed by the service.
"""
from functools import lru_cache
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines the application-wide configuration settings.

    Attributes:
        DATABASE_URL: The connection string for the PostgreSQL database.
        MINIO_ENDPOINT: The endpoint URL for the MinIO server.
        MINIO_ACCESS_KEY: The access key for MinIO authentication.
        MINIO_SECRET_KEY: The secret key for MinIO authentication.
        MINIO_MODEL_BUCKET_NAME: The MinIO bucket for storing model artifacts.
        MINIO_VALIDATION_REPORTS_BUCKET_NAME: The MinIO bucket for validation reports.
        KUBERNETES_CONFIG_PATH: Optional path to the kubeconfig file. If None,
                                in-cluster config is used.
        KUBERNETES_NAMESPACE_MODELS: The K8s namespace for deploying models.
        SECURITY_SCANNER_API_ENDPOINT: Optional endpoint for a security scanning service.
        SECURITY_SCANNER_API_KEY: Optional API key for the security scanner.
        MLFLOW_TRACKING_URI: Optional URI for an MLflow tracking server.
        LOG_LEVEL: The logging level for the application.
        INTERNAL_API_KEY: A secret key to secure internal service-to-service communication.
    """
    DATABASE_URL: str
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: SecretStr
    MINIO_MODEL_BUCKET_NAME: str = "ml-models"
    MINIO_VALIDATION_REPORTS_BUCKET_NAME: str = "validation-reports"

    KUBERNETES_CONFIG_PATH: Optional[str] = None
    KUBERNETES_NAMESPACE_MODELS: str = "ml-models-serving"

    SECURITY_SCANNER_API_ENDPOINT: Optional[str] = None
    SECURITY_SCANNER_API_KEY: Optional[SecretStr] = None

    MLFLOW_TRACKING_URI: Optional[str] = None
    
    LOG_LEVEL: str = "INFO"
    INTERNAL_API_KEY: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get a singleton instance of the Settings object.

    Using lru_cache ensures the settings are loaded only once.

    Returns:
        An instance of the Settings class.
    """
    return Settings()