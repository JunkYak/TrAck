"""
app/database/base.py
--------------------
Declares the shared SQLAlchemy :class:`Base` from which all ORM models inherit.

Importing this module early (before any model modules) ensures Alembic's
``autogenerate`` can discover all tables via ``Base.metadata``.
"""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

# ---------------------------------------------------------------------------
# Naming convention
# ---------------------------------------------------------------------------
# Alembic's autogenerate uses these names when creating constraints.
# Having explicit names avoids unnamed constraints in migration scripts,
# which cause problems on databases that require constraint names (e.g. PG).
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    """Project-wide declarative base.

    * Applies the constraint naming convention automatically.
    * Provides a default ``__tablename__`` derived from the class name so
      subclasses can opt-in to the convention without repeating themselves.
    """

    metadata = metadata

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:  # type: ignore[override]
        """Snake-case the class name and pluralise naively.

        ``User``   → ``users``
        ``UserLog`` → ``user_logs``

        Override per-model when the default is not suitable.
        """
        import re

        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return f"{name}s"
