"""
app/models/user.py
------------------
SQLAlchemy ORM model for the ``users`` table.

Fields are designed around Google OAuth as the primary authentication
provider: ``google_id`` and ``email`` are both unique, and ``profile_picture``
stores the Google avatar URL.

The model inherits the auto-generated ``__tablename__`` (→ ``users``) and the
constraint naming convention from :class:`app.database.base.Base`.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class User(Base):
    """Represents an authenticated user of the Track application."""

    # ------------------------------------------------------------------ #
    # Primary key
    # ------------------------------------------------------------------ #
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        doc="UUID v4 stored as a 36-char string for SQLite compatibility.",
    )

    # ------------------------------------------------------------------ #
    # Google OAuth identifiers
    # ------------------------------------------------------------------ #
    google_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique subject identifier returned by Google.",
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
        doc="User's primary e-mail address from Google.",
    )

    # ------------------------------------------------------------------ #
    # Profile
    # ------------------------------------------------------------------ #
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Display name from Google profile.",
    )
    profile_picture: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
        doc="URL to the Google profile avatar.",
    )

    # ------------------------------------------------------------------ #
    # Timestamps & flags
    # ------------------------------------------------------------------ #
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
        doc="When the user record was first created.",
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="Timestamp of the user's most recent login.",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Soft-delete / deactivation flag.",
    )

    # ------------------------------------------------------------------ #
    # Relationships
    # ------------------------------------------------------------------ #
    weight_logs = relationship(
        "WeightLog", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    measurement_sessions = relationship(
        "MeasurementSession", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    exercises = relationship(
        "Exercise", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    exercise_logs = relationship(
        "ExerciseLog", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    recipes = relationship(
        "Recipe", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    meal_templates = relationship(
        "MealTemplate", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    daily_nutrition_logs = relationship(
        "DailyNutritionLog", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    # ------------------------------------------------------------------ #
    # Dunder helpers
    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:
        return f"<User id={self.id!r} email={self.email!r}>"

