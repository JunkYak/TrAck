"""
app/core/exceptions.py
----------------------
Domain-level exceptions for the Track application.

These are *not* HTTP exceptions – translation to HTTP responses happens in the
exception handlers registered in app/main.py.  This keeps business logic free
from framework concerns (Single Responsibility / Dependency Inversion).
"""

from __future__ import annotations


class TrackBaseException(Exception):
    """Root exception for all Track domain errors."""

    default_message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


# ---------------------------------------------------------------------------
# Resource errors
# ---------------------------------------------------------------------------
class NotFoundError(TrackBaseException):
    """Raised when a requested resource does not exist."""

    default_message = "The requested resource was not found."


class AlreadyExistsError(TrackBaseException):
    """Raised when creating a resource that already exists."""

    default_message = "The resource already exists."


# ---------------------------------------------------------------------------
# Auth errors
# ---------------------------------------------------------------------------
class AuthenticationError(TrackBaseException):
    """Raised for invalid credentials or expired tokens."""

    default_message = "Authentication failed."


class AuthorizationError(TrackBaseException):
    """Raised when a user lacks permission for an action."""

    default_message = "You do not have permission to perform this action."


class TokenError(TrackBaseException):
    """Raised for invalid, malformed, or expired JWT tokens."""

    default_message = "Invalid or expired token."


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------
class ValidationError(TrackBaseException):
    """Raised for business-rule validation failures (not Pydantic errors)."""

    default_message = "Validation failed."
