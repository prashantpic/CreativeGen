from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Centralized application configuration settings.
    Loads settings from environment variables and/or a .env file.
    """
    
    # --- Odoo Configuration ---
    ODOO_URL: str
    ODOO_DB: str
    ODOO_USERNAME: str
    ODOO_PASSWORD: SecretStr
    
    # --- Main Application Database Configuration ---
    # Used to read user context (e.g., odoo_partner_id)
    DATABASE_URL: SecretStr
    
    # --- Payment Gateway Keys (Conditional Usage) ---
    # These are only used if the adapter needs to make direct calls to Stripe/PayPal,
    # bypassing Odoo's direct orchestration for specific flows.
    STRIPE_API_KEY: Optional[SecretStr] = None
    PAYPAL_CLIENT_ID: Optional[SecretStr] = None
    PAYPAL_CLIENT_SECRET: Optional[SecretStr] = None
    
    # --- Internal Service Security ---
    # An optional API key for securing service-to-service communication.
    INTERNAL_SERVICE_API_KEY: Optional[SecretStr] = None
    
    # --- Operational Settings ---
    LOG_LEVEL: str = "INFO"

    # --- Feature Toggles ---
    # Set to true to enable direct calls from this adapter to Stripe's API.
    ENABLE_DIRECT_STRIPE_CALLS: bool = False
    # Set to true to enable direct calls from this adapter to PayPal's API.
    ENABLE_DIRECT_PAYPAL_CALLS: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",        # Load from .env file for local development
        env_file_encoding='utf-8',
        extra="ignore"          # Ignore extra environment variables
    )

# Instantiate a single, globally accessible settings object.
settings = Settings()