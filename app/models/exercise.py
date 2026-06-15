"""
app/models/exercise.py
----------------------
SQLAlchemy ORM model for the ``exercises`` table.

Represents a user-created exercise definition.  Exercises are never
hard-deleted through normal application flows — they are soft-deleted
via the ``is_archived`` flag so that historical logs remain intact.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Exercise(Base):
    """A user-created exercise definition."""

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_exercises_user_name"),
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
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------ #
    # Payload
    # ------------------------------------------------------------------ #
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="User-defined exercise name.",
    )
    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Soft-delete flag. Archived exercises are hidden from default lists.",
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
        doc="Last modification timestamp.",
    )

    # ------------------------------------------------------------------ #
    # Relationships
    # ------------------------------------------------------------------ #
    user = relationship("User", back_populates="exercises", lazy="selectin")
    logs = relationship(
        "ExerciseLog",
        back_populates="exercise",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Exercise id={self.id!r} name={self.name!r} archived={self.is_archived}>"
