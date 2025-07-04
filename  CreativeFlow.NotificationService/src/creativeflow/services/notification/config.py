"""
Application configuration management using Pydantic.

This module defines a `Settings` class that loads all required configuration
from environment variables. Pydantic automatically validates the data, ensuring
that the application does not start with a missing or invalid configuration.
"""
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field, validator


class Settings(BaseModel):
    """
    Pydantic model for application settings, loaded from environment variables.
    Provides validation to ensure required settings are present for enabled features.
    """
    # General
    LOG_LEVEL: str = Field("INFO", description="The logging level for the application.")

    # Feature Toggles
    ENABLE_RABBITMQ_CONSUMER: bool = Field(True, description="Enable the RabbitMQ message consumer.")
    ENABLE_REDIS_CONSUMER: bool = Field(False, description="Enable the Redis Pub/Sub message consumer.")
    ENABLE_APNS_PUSH: bool = Field(True, description="Enable sending push notifications via APNS.")
    ENABLE_FCM_PUSH: bool = Field(True, description="Enable sending push notifications via FCM.")

    # RabbitMQ Configuration
    RABBITMQ_URL: str = Field("amqp://guest:guest@localhost:5672/%2F", description="URL for RabbitMQ connection.")
    RABBITMQ_QUEUE_NAME_AI_UPDATES: str = Field("ai_updates_notifications", description="Queue name for AI generation updates.")

    # Redis Configuration
    REDIS_URL: str = Field("redis://localhost:6379/0", description="URL for Redis connection.")
    REDIS_PUBSUB_CHANNEL_NAME: str = Field("general_notifications", description="Redis Pub/Sub channel for general notifications.")

    # APNS (Apple Push Notification Service) Configuration
    APNS_KEY_ID: Optional[str] = Field(None, description="Your APNS key ID.")
    APNS_TEAM_ID: Optional[str] = Field(None, description="Your Apple Team ID.")
    APNS_CERT_FILE: Optional[str] = Field(None, description="Path to your .p8 key file for APNS.")
    APNS_USE_SANDBOX: bool = Field(False, description="Use APNS sandbox environment for development.")

    # FCM (Firebase Cloud Messaging) Configuration
    FCM_API_KEY: Optional[str] = Field(None, description="Your FCM server key.")

    @validator("APNS_KEY_ID", "APNS_TEAM_ID", "APNS_CERT_FILE", always=True)
    def check_apns_config(cls, v, values):
        """Validator to ensure APNS settings are present if APNS is enabled."""
        if values.get("ENABLE_APNS_PUSH") and not v:
            raise ValueError("APNS_KEY_ID, APNS_TEAM_ID, and APNS_CERT_FILE must be set if ENABLE_APNS_PUSH is True.")
        return v

    @validator("FCM_API_KEY", always=True)
    def check_fcm_config(cls, v, values):
        """Validator to ensure FCM settings are present if FCM is enabled."""
        if values.get("ENABLE_FCM_PUSH") and not v:
            raise ValueError("FCM_API_KEY must be set if ENABLE_FCM_PUSH is True.")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.

    This function returns a cached instance of the Settings model, ensuring that
    environment variables are read and validated only once.

    Returns:
        A cached instance of the Settings class.
    """
    return Settings()