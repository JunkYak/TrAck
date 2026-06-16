"""
app/models/nutrition_log.py
---------------------------
SQLAlchemy ORM models for DailyNutritionLog, DailyNutritionLogEntry,
and DailyNutritionLogItem.

Represents immutable historical snapshots of daily nutrition.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import List

from sqlalchemy import Date, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DailyNutritionLog(Base):
    """The root container for a single day's nutrition tracking."""

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_daily_logs_user_date"),
    )

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

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
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

    entries: Mapped[List["DailyNutritionLogEntry"]] = relationship(
        "DailyNutritionLogEntry",
        back_populates="log",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    user = relationship("User", back_populates="daily_nutrition_logs")
    __tablename__ = "daily_nutrition_logs"


class DailyNutritionLogEntry(Base):
    """A grouping layer representing the 'event' (e.g., Breakfast Shake)."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    log_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("daily_nutrition_logs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    entry_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    entry_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="FOOD, RECIPE, TEMPLATE, or CUSTOM",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
    )

    log: Mapped["DailyNutritionLog"] = relationship("DailyNutritionLog", back_populates="entries")
    items: Mapped[List["DailyNutritionLogItem"]] = relationship(
        "DailyNutritionLogItem",
        back_populates="entry",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    __tablename__ = "daily_nutrition_log_entries"


class DailyNutritionLogItem(Base):
    """An immutable snapshot of a food ingredient consumed."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    entry_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("daily_nutrition_log_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Snapshot fields - disconnected from the original catalog
    food_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(10), nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    protein: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
    )
    __tablename__ = "daily_nutrition_log_items"

    entry: Mapped["DailyNutritionLogEntry"] = relationship("DailyNutritionLogEntry", back_populates="items")
