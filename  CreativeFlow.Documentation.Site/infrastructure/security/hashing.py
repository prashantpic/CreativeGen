```python
from passlib.context import CryptContext

# Use bcrypt as it is a strong and widely used hashing algorithm.
# schemes=["bcrypt"] is sufficient for new applications.
# deprecated="auto" will handle upgrading hashes if you add new schemes later.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_secret(secret: str) -> str:
    """
    Hashes a given secret using the configured hashing algorithm.

    Args:
        secret: The plaintext secret to hash.

    Returns:
        The hashed secret string.
    """
    return pwd_context.hash(secret)


def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    """
    Verifies a plaintext secret against a stored hash.

    Args:
        plain_secret: The plaintext secret provided by the user.
        hashed_secret: The stored hash to verify against.

    Returns:
        True if the secret is valid, False otherwise.
    """
    return pwd_context.verify(plain_secret, hashed_secret)
```