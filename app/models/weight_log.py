"""
app/models/weight_log.py
------------------------
SQLAlchemy ORM model for the ``weight_logs`` table.

Tracks a user's daily body-weight entries.  The ``(user_id, date)`` pair
is unique so only one reading per day is stored (upsert semantics in the
service layer).
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WeightLog(Base):
    """A single daily weight reading for a user."""

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_weight_logs_user_date"),
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
        doc="Calendar date of the weigh-in.",
    )
    weight_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Body weight in kilograms.",
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
    user = relationship("User", back_populates="weight_logs", lazy="selectin")

    def __repr__(self) -> str:
        return f"<WeightLog id={self.id!r} user={self.user_id!r} date={self.date}>"
