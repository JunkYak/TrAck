"""
app/models/cardio.py
--------------------
SQLAlchemy ORM models for Cardio domain.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class RunType(str, enum.Enum):
    EASY = "EASY"
    TEMPO_INTERVAL = "TEMPO_INTERVAL"
    LONG = "LONG"


class CardioSession(Base):
    """A user-owned cardio session representing a single run."""

    __tablename__ = "cardio_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    run_type: Mapped[RunType] = mapped_column(
        Enum(RunType, native_enum=False),
        nullable=False,
    )

    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    duration_minutes: Mapped[float] = mapped_column(Float, nullable=False)
    average_pace: Mapped[float] = mapped_column(Float, nullable=False)
    body_weight_used: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_calories: Mapped[float] = mapped_column(Float, nullable=False)

    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    performed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
    )

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

    user = relationship("User")
