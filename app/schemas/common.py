"""
app/schemas/common.py
---------------------
Shared Pydantic schemas used across the application.
"""

from __future__ import annotations

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Base model config
# ---------------------------------------------------------------------------
class AppBaseModel(BaseModel):
    """Base for all application schemas.

    * ``from_attributes=True`` enables building schemas from ORM objects.
    * ``populate_by_name=True`` lets callers use either the field name or alias.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# ---------------------------------------------------------------------------
# Generic paginated response
# ---------------------------------------------------------------------------
class PaginatedResponse(AppBaseModel, Generic[T]):
    """Wrap a list of items with pagination metadata."""

    items: List[T]
    total: int
    limit: int
    offset: int

    @property
    def has_more(self) -> bool:
        return self.offset + self.limit < self.total


# ---------------------------------------------------------------------------
# Generic message response
# ---------------------------------------------------------------------------
class MessageResponse(AppBaseModel):
    """Simple acknowledgement / message payload."""

    message: str
    detail: Optional[Any] = None


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
class HealthResponse(AppBaseModel):
    """Response body for the /health endpoint."""

    status: str = "ok"
    app: str
    version: str
    environment: str
    database: str = "ok"
