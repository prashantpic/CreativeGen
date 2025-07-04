"""
Defines Pydantic schemas for shared configuration structures.

This allows for validation and type-hinting of configuration objects used by
services. These schemas use `pydantic_settings.BaseSettings` to enable
automatic loading from environment variables.
"""
from pydantic import AmqpDsn, HttpUrl, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfigSchema(BaseSettings):
    """Base configuration schema with common settings."""

    # All environment variables will be prefixed (e.g., APP_ENVIRONMENT)
    # Nested models can be defined with a double underscore (e.g., APP_DATABASE__URL)
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_nested_delimiter="__", extra="ignore"
    )

    environment: str = "development"


class DatabaseConfigSchema(BaseSettings):
    """Schema for database connection settings."""

    url: PostgresDsn
    pool_size: int = 5
    max_overflow: int = 10


class RedisConfigSchema(BaseSettings):
    """Schema for Redis connection settings."""

    host: str
    port: int = 6379
    password: SecretStr | None = None
    db: int = 0


class RabbitMQConfigSchema(BaseSettings):
    """Schema for RabbitMQ connection settings."""

    url: AmqpDsn  # e.g., amqp://user:pass@host:port/vhost


class ServiceEndpointSchema(BaseSettings):
    """Schema for defining an internal or external service endpoint."""

    url: HttpUrl
    timeout_seconds: int = 30


class ThirdPartyServiceConfigSchema(BaseSettings):
    """Schema for a generic third-party service configuration."""

    api_key: SecretStr
    base_url: HttpUrl


class LoggingConfigSchema(BaseSettings):
    """Schema for logging configuration."""

    level: str = "INFO"
    service_name: str  # Must be set by each service


class SentryConfigSchema(BaseSettings):
    """Schema for Sentry error tracking configuration."""

    dsn: HttpUrl | None = None
    release_version: str | None = None