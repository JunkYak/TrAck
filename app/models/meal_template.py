"""
app/models/meal_template.py
---------------------------
SQLAlchemy ORM models for MealTemplates.

MealTemplates are high-level user-scoped collections that can contain both
individual FoodItems and entire Recipes.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MealTemplate(Base):
    """A reusable meal configuration containing foods and/or recipes."""

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_meal_templates_user_name"),
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

    # ------------------------------------------------------------------ #
    # Relationships
    # ------------------------------------------------------------------ #
    foods: Mapped[List["MealTemplateFood"]] = relationship(
        "MealTemplateFood",
        back_populates="meal_template",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    recipes: Mapped[List["MealTemplateRecipe"]] = relationship(
        "MealTemplateRecipe",
        back_populates="meal_template",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    user = relationship("User", back_populates="meal_templates")

    def __repr__(self) -> str:
        return f"<MealTemplate id={self.id!r} name={self.name!r} user={self.user_id!r}>"


class MealTemplateFood(Base):
    """A specific quantity of a FoodItem belonging to a MealTemplate."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    meal_template_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("meal_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    food_item_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("food_items.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    meal_template: Mapped["MealTemplate"] = relationship("MealTemplate", back_populates="foods")
    food_item = relationship("FoodItem")


class MealTemplateRecipe(Base):
    """A specific quantity/multiplier of a Recipe belonging to a MealTemplate."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    meal_template_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("meal_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    recipe_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    multiplier: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    meal_template: Mapped["MealTemplate"] = relationship("MealTemplate", back_populates="recipes")
    recipe = relationship("Recipe")
