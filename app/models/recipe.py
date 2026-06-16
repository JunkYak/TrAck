"""
app/models/recipe.py
--------------------
SQLAlchemy ORM models for the ``recipes`` and ``recipe_ingredients`` tables.

Recipes are user-scoped collections of FoodItems. They cannot contain other
recipes. The relationship to FoodItems uses RESTRICT to prevent deletion of
foods that are actively used in recipes.
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


class Recipe(Base):
    """A user-scoped collection of food items."""

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_recipes_user_name"),
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
    ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    user = relationship("User", back_populates="recipes")

    def __repr__(self) -> str:
        return f"<Recipe id={self.id!r} name={self.name!r} user={self.user_id!r}>"


class RecipeIngredient(Base):
    """A specific quantity of a FoodItem belonging to a Recipe."""

    __table_args__ = (
        UniqueConstraint("recipe_id", "food_item_id", name="uq_recipe_ingredients_recipe_food"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    recipe_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Use RESTRICT so we don't accidentally delete foods used in recipes.
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

    # ------------------------------------------------------------------ #
    # Relationships
    # ------------------------------------------------------------------ #
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
    food_item = relationship("FoodItem")

    def __repr__(self) -> str:
        return f"<RecipeIngredient recipe={self.recipe_id!r} food={self.food_item_id!r}>"
