```python
from functools import lru_cache
from typing import Optional

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manages application configuration settings.
    Loads values from environment variables or a .env file.
    """
    # Core settings
    LOG_LEVEL: str = "INFO"
    
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dev_platform_db"
    
    # Messaging settings
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_WEBHOOK_EXCHANGE_NAME: str = "webhook_events_exchange"
    RABBITMQ_WEBHOOK_ROUTING_KEY_PREFIX: str = "webhook.event"
    
    # Cache/Rate Limiting settings
    REDIS_URL: str = "redis://localhost:6379"
    DEFAULT_RATE_LIMIT_REQUESTS: int = 100
    DEFAULT_RATE_LIMIT_PERIOD_SECONDS: int = 60

    # Security settings
    JWT_SECRET_KEY: str = "a_very_secret_key_for_jwt" # For user auth on management endpoints
    API_KEY_HEADER_NAME: str = "X-API-KEY"
    
    # External Service URLs
    AI_GENERATION_SERVICE_URL: HttpUrl = "http://localhost:8001/api/v1"
    ASSET_MANAGEMENT_SERVICE_URL: HttpUrl = "http://localhost:8002/api/v1"
    USER_TEAM_SERVICE_URL: HttpUrl = "http://localhost:8003/api/v1"
    AUTH_SERVICE_URL: Optional[HttpUrl] = None # For future user token validation
    
    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    Using lru_cache ensures the settings are loaded only once.
    """
    return Settings()
```