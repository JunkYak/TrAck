"""
app/schemas/user.py
-------------------
Pydantic schemas for the User domain.

Schema hierarchy
~~~~~~~~~~~~~~~~
* ``UserBase``      – shared readable fields.
* ``UserCreate``    – fields required when creating a user from Google OAuth.
* ``UserUpdate``    – optional fields that may be patched.
* ``UserRead``      – full representation returned to clients.
* ``UserInDB``      – internal variant that includes audit/status columns.

All schemas inherit :class:`app.schemas.common.AppBaseModel` which sets
``from_attributes=True`` for seamless ORM → schema conversion.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field

from app.schemas.common import AppBaseModel


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class UserBase(AppBaseModel):
    """Fields common to every user representation."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    profile_picture: Optional[str] = None


# ---------------------------------------------------------------------------
# Create (input from Google OAuth flow)
# ---------------------------------------------------------------------------
class UserCreate(UserBase):
    """Payload used when creating a new user from a Google sign-in."""

    google_id: str = Field(..., min_length=1, max_length=255)


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
class UserUpdate(AppBaseModel):
    """Partial update – every field is optional."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    profile_picture: Optional[str] = None
    is_active: Optional[bool] = None


# ---------------------------------------------------------------------------
# Read (API response)
# ---------------------------------------------------------------------------
class UserRead(UserBase):
    """Public-facing user representation returned by API endpoints."""

    id: str
    google_id: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool


# ---------------------------------------------------------------------------
# Internal DB representation
# ---------------------------------------------------------------------------
class UserInDB(UserRead):
    """Extended read schema that mirrors the full database row.

    Identical to ``UserRead`` for now but kept as a separate class so
    internal-only fields can be added later without leaking them to clients.
    """
