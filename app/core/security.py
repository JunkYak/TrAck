"""
app/core/security.py
--------------------
JWT creation / verification and password hashing utilities.

This module has NO business logic – it is a pure utility layer used by the
auth service.  Google OAuth token exchange lives in app/auth/oauth.py.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Return the bcrypt hash of *plain*."""
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return ``True`` if *plain* matches the stored *hashed* password."""
    return _pwd_context.verify(plain, hashed)


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------
def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    """Encode a JWT with the given payload and expiry."""
    payload = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    payload.update({"exp": expire, "iat": datetime.now(tz=timezone.utc)})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: str | int, extra: dict[str, Any] | None = None) -> str:
    """Create a short-lived access token for *subject* (typically user id)."""
    data: dict[str, Any] = {"sub": str(subject), "type": "access"}
    if extra:
        data.update(extra)
    return _create_token(data, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(subject: str | int) -> str:
    """Create a long-lived refresh token for *subject*."""
    data: dict[str, Any] = {"sub": str(subject), "type": "refresh"}
    return _create_token(data, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT.

    Raises:
        jose.JWTError: If the token is invalid or expired.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
