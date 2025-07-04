from passlib.context import CryptContext

# Use bcrypt as the default hashing algorithm.
# It is a strong, widely-used, and well-vetted choice for secrets.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_secret(secret: str) -> str:
    """
    Hashes a given plaintext secret.

    Args:
        secret: The plaintext secret string to hash.

    Returns:
        The hashed secret string.
    """
    return pwd_context.hash(secret)


def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    """
    Verifies a plaintext secret against a stored hash.

    Args:
        plain_secret: The plaintext secret to verify.
        hashed_secret: The stored hash to compare against.

    Returns:
        True if the secret matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_secret, hashed_secret)