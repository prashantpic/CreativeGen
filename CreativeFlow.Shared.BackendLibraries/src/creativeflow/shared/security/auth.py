"""
Provides shared security utilities, such as JWT decoding and permission-checking
helpers (FastAPI dependencies), to be used by various backend services.
"""
import os
from typing import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from ..core.exceptions import AuthenticationException, PermissionDeniedException

# This scheme can be used in FastAPI route dependencies to extract the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token", auto_error=False)

# It's crucial to load these from environment variables in a real application.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "a_secure_secret_key_for_development")
ALGORITHM = "HS256"


class TokenPayload(BaseModel):
    """Schema for the data encoded within the JWT."""
    sub: str  # Subject, typically the User ID
    roles: list[str] = []
    exp: int  # Expiration time claim


async def get_current_user(token: str | None = Depends(oauth2_scheme)) -> TokenPayload:
    """
    FastAPI dependency to decode and validate a JWT from the Authorization header.

    This function is the cornerstone of API authentication. It attempts to decode the
    provided bearer token and validates its structure against the TokenPayload model.

    Raises:
        AuthenticationException: If the token is missing, invalid, expired, or the
                                 payload cannot be parsed.

    Returns:
        The validated token payload containing user ID and roles.
    """
    if token is None:
        raise AuthenticationException(detail="Not authenticated")

    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        # Validate the structure and types of the decoded payload
        token_data = TokenPayload(**payload)
    except JWTError:
        # This catches signature errors, expired tokens, etc.
        raise AuthenticationException(detail="Could not validate credentials, token is invalid or expired.")
    except ValidationError:
        # This catches cases where the payload is valid JWT but malformed.
        raise AuthenticationException(detail="Could not validate credentials, token payload is malformed.")

    return token_data


def require_role(required_role: str) -> Callable[[TokenPayload], TokenPayload]:
    """
    Factory for a FastAPI dependency that checks if a user has a specific role.

    This allows protecting routes with role-based access control (RBAC) in a
    declarative way.

    Example:
        @app.post("/", dependencies=[Depends(require_role("admin"))])
        async def create_something_for_admins():
            ...

    Args:
        required_role: The role string that the user must possess.

    Returns:
        A FastAPI dependency function that performs the role check.
    """
    async def role_checker(current_user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        """The actual dependency function that will be executed by FastAPI."""
        if required_role not in current_user.roles:
            raise PermissionDeniedException(
                detail=f"User lacks required role: '{required_role}'"
            )
        return current_user

    return role_checker