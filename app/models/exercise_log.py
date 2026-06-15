"""
app/models/exercise_log.py
--------------------------
SQLAlchemy ORM model for the ``exercise_logs`` table.

Stores one best-set entry per exercise per date.  The
``(user_id, exercise_id, log_date)`` triple is unique so upsert
semantics can be applied in the service layer.

The ``exercise_id`` foreign key uses ``RESTRICT`` to prevent accidental
hard-deletion of exercises that have historical log data.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ExerciseLog(Base):
    """A single best-set log entry for an exercise on a given date."""

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "exercise_id",
            "log_date",
            name="uq_exercise_logs_user_exercise_date",
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
    # Foreign keys
    # ------------------------------------------------------------------ #
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercise_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("exercises.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------ #
    # Payload
    # ------------------------------------------------------------------ #
    log_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Calendar date of the log entry.",
    )
    weight_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Weight used in the best set (kilograms).",
    )
    reps: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Repetitions in the best set.",
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
        doc="Optional free-text notes.",
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
    user = relationship("User", back_populates="exercise_logs", lazy="selectin")
    exercise = relationship("Exercise", back_populates="logs", lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"<ExerciseLog id={self.id!r} exercise={self.exercise_id!r} "
            f"date={self.log_date}>"
        )
