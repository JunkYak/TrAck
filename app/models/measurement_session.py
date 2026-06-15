"""
app/models/measurement_session.py
---------------------------------
SQLAlchemy ORM model for the ``measurement_sessions`` table.

Tracks weekly body measurements (waist, bicep, quad) in inches.
The ``(user_id, date)`` pair is unique so only one session per day is stored.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MeasurementSession(Base):
    """A single weekly measurement session for a user."""

    __table_args__ = (
        UniqueConstraint(
            "user_id", "date", name="uq_measurement_sessions_user_date"
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
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------ #
    # Payload
    # ------------------------------------------------------------------ #
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Calendar date of the measurement session.",
    )
    waist_in: Mapped[float | None] = mapped_column(
        Float, nullable=True, doc="Waist circumference in inches."
    )
    bicep_in: Mapped[float | None] = mapped_column(
        Float, nullable=True, doc="Bicep circumference in inches."
    )
    quad_in: Mapped[float | None] = mapped_column(
        Float, nullable=True, doc="Quad circumference in inches."
    )

    # ------------------------------------------------------------------ #
    # Audit
    # ------------------------------------------------------------------ #
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
    )

    # ------------------------------------------------------------------ #
    # Relationships
    # ------------------------------------------------------------------ #
    user = relationship(
        "User", back_populates="measurement_sessions", lazy="selectin"
    )

    def __repr__(self) -> str:
        return (
            f"<MeasurementSession id={self.id!r} user={self.user_id!r} "
            f"date={self.date}>"
        )
