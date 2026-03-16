"""FastAPI dependency injection functions."""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token

security_scheme = HTTPBearer()


class CurrentUser:
    """Decoded user information from JWT token."""

    def __init__(self, id: UUID, role: str) -> None:
        self.id = id
        self.role = role


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),  # noqa: B008
) -> CurrentUser:
    """Extract and validate the current user from the JWT token."""
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    try:
        user_id = UUID(payload["sub"])
        role = payload["role"]
    except (KeyError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        ) from err
    return CurrentUser(id=user_id, role=role)


def require_role(*allowed_roles: str):
    """Dependency factory that restricts access to specific roles."""

    async def role_checker(
        current_user: CurrentUser = Depends(get_current_user),  # noqa: B008
    ) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not authorized for this action",
            )
        return current_user

    return role_checker
