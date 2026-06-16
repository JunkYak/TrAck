"""
app/models/food_item.py
-----------------------
SQLAlchemy ORM model for the ``food_items`` table.

Represents the foundation of the nutrition tracking domain.
Supports both globally shared foods (user_id = NULL) and user-owned
overrides (user_id populated).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class FoodItem(Base):
    """A food item, either from the global catalog or a user override."""

    __table_args__ = (
        Index(
            "ix_food_items_user_name_unit",
            "user_id",
            "name",
            "unit",
            unique=True,
            sqlite_where=text("user_id IS NOT NULL"),
        ),
        Index(
            "ix_food_items_global_name_unit",
            "name",
            "unit",
            unique=True,
            sqlite_where=text("user_id IS NULL"),
        ),
    )

    # ------------------------------------------------------------------ #
    # Primary key
    # ------------------------------------------------------------------ #
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ------------------------------------------------------------------ #
    # Foreign key
    # ------------------------------------------------------------------ #
    user_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        doc="NULL means global food. Populated means user override.",
    )

    # ------------------------------------------------------------------ #
    # Payload
    # ------------------------------------------------------------------ #
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    unit: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="Supported units: g, ml, count",
    )
    calories_per_unit: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    protein_per_unit: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Source of the data: AI or MANUAL",
    )

    # ------------------------------------------------------------------ #
    # Audit
    # ------------------------------------------------------------------ #
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        onupdate=_utcnow,
    )

    def __repr__(self) -> str:
        return f"<FoodItem id={self.id!r} name={self.name!r} user={self.user_id!r}>"
