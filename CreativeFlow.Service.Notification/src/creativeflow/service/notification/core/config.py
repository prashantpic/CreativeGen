from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application configuration settings, loaded from environment variables.
    
    Pydantic's BaseSettings provides type-checking and validation for all
    configuration parameters, ensuring the application starts with a valid
    and predictable configuration state.
    """
    # Service
    LOG_LEVEL: str = "INFO"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    NOTIFICATION_QUEUE_NAME: str = "notification_events"

    # Apple Push Notification Service (APNS)
    APNS_ENABLED: bool = False
    APNS_KEY_ID: str = ""
    APNS_TEAM_ID: str = ""
    APNS_AUTH_KEY_PATH: str = ""  # Path to the .p8 key file
    APNS_TOPIC: str = ""          # Typically the app's bundle ID
    APNS_USE_SANDBOX: bool = True

    # Firebase Cloud Messaging (FCM)
    FCM_ENABLED: bool = False
    FCM_PROJECT_ID: str = ""
    FCM_CREDENTIALS_PATH: str = "" # Path to the service account JSON file

    class Config:
        # Pydantic will read configuration from a .env file
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.
    
    The lru_cache decorator ensures that the Settings object is created
    only once, preventing repeated file I/O and environment variable parsing.
    
    Returns:
        The application settings object.
    """
    return Settings()