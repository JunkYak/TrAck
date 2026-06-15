"""
app/repositories/user.py
------------------------
Data-access layer for :class:`User` entities.

Extends the generic :class:`BaseRepository` with look-up methods specific
to the User domain (by Google ID, by e-mail, active-only filters).

All queries are async and operate within the session supplied at
construction time – the repository has *no* knowledge of how or when the
session is committed (Single Responsibility).
"""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, str]):
    """Repository for :class:`User` ORM entities.

    The ``str`` type parameter corresponds to the UUID primary key stored as
    a 36-character string.
    """

    model = User

    # ------------------------------------------------------------------ #
    # Constructors
    # ------------------------------------------------------------------ #
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    # ------------------------------------------------------------------ #
    # Domain-specific reads
    # ------------------------------------------------------------------ #
    async def get_by_google_id(self, google_id: str) -> Optional[User]:
        """Return the user matching the Google subject ID, or ``None``."""
        return await self.get_one_by(google_id=google_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Return the user matching the given e-mail address, or ``None``."""
        return await self.get_one_by(email=email)

    async def get_active_users(
        self, *, limit: int = 100, offset: int = 0
    ) -> Sequence[User]:
        """Return a page of active (non-deactivated) users."""
        stmt = (
            select(User)
            .where(User.is_active.is_(True))
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def exists_by_email(self, email: str) -> bool:
        """Return ``True`` if a user with the given e-mail already exists."""
        return (await self.get_by_email(email)) is not None

    async def exists_by_google_id(self, google_id: str) -> bool:
        """Return ``True`` if a user with the given Google ID already exists."""
        return (await self.get_by_google_id(google_id)) is not None
