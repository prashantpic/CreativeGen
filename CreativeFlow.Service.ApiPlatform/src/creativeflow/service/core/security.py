import secrets
from passlib.context import CryptContext

# Configure the password context for hashing with bcrypt
# This is the standard for securely hashing secrets and passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the length of the generated key and secret for security and usability
API_KEY_LENGTH = 32  # e.g., cf_ + 32 chars
API_SECRET_LENGTH = 48 # e.g., 48 chars


def generate_api_key_and_secret() -> tuple[str, str]:
    """
    Generates a new public API key and a plain text secret.

    The API key has a 'cf_' prefix for easy identification.
    The secret is a longer, cryptographically secure random string.

    Returns:
        A tuple containing the public API key and the plain text secret.
        The secret should only be shown to the user once upon creation.
    """
    api_key = f"cf_{secrets.token_urlsafe(API_KEY_LENGTH)}"
    secret = secrets.token_urlsafe(API_SECRET_LENGTH)
    return api_key, secret


def hash_api_secret(secret: str) -> str:
    """
    Hashes a plain text API secret using the configured password context.

    Args:
        secret: The plain text secret to hash.

    Returns:
        The hashed secret string, suitable for storing in the database.
    """
    return pwd_context.hash(secret)


def verify_api_secret(plain_secret: str, hashed_secret: str) -> bool:
    """
    Verifies a plain text secret against its hashed version.

    Args:
        plain_secret: The plain text secret provided by the user/client.
        hashed_secret: The hashed secret stored in the database.

    Returns:
        True if the secret is valid, False otherwise.
    """
    return pwd_context.verify(plain_secret, hashed_secret)