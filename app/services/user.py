"""
app/services/user.py
--------------------
Business-logic layer for the User domain.

Responsibilities
~~~~~~~~~~~~~~~~
* Orchestrate CRUD operations via :class:`UserRepository`.
* Enforce domain rules (uniqueness, activation, etc.).
* Raise domain exceptions – *never* HTTP exceptions.

The service receives its repository through constructor injection
(Dependency Inversion Principle) so it can be tested with a mock
repository.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Sequence

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UserService(BaseService):
    """High-level operations on :class:`User` entities."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    async def get_by_id(self, user_id: str) -> User:
        """Return a user by primary key or raise :class:`NotFoundError`."""
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User with id '{user_id}' not found.")
        return user

    async def get_by_email(self, email: str) -> User:
        """Return a user by e-mail or raise :class:`NotFoundError`."""
        user = await self._repo.get_by_email(email)
        if user is None:
            raise NotFoundError(f"User with email '{email}' not found.")
        return user

    async def get_by_google_id(self, google_id: str) -> User:
        """Return a user by Google subject ID or raise :class:`NotFoundError`."""
        user = await self._repo.get_by_google_id(google_id)
        if user is None:
            raise NotFoundError(f"User with google_id '{google_id}' not found.")
        return user

    async def list_users(
        self, *, limit: int = 100, offset: int = 0, active_only: bool = False
    ) -> Sequence[User]:
        """Return a paginated list of users."""
        if active_only:
            return await self._repo.get_active_users(limit=limit, offset=offset)
        return await self._repo.get_all(limit=limit, offset=offset)

    # ------------------------------------------------------------------ #
    # Writes
    # ------------------------------------------------------------------ #
    async def create_user(self, data: UserCreate) -> User:
        """Create a new user from Google OAuth data.

        Raises :class:`AlreadyExistsError` if the ``google_id`` or ``email``
        is already taken.
        """
        if await self._repo.exists_by_google_id(data.google_id):
            raise AlreadyExistsError(
                f"User with google_id '{data.google_id}' already exists."
            )
        if await self._repo.exists_by_email(data.email):
            raise AlreadyExistsError(
                f"User with email '{data.email}' already exists."
            )

        user = User(
            google_id=data.google_id,
            email=data.email,
            name=data.name,
            profile_picture=data.profile_picture,
        )
        return await self._repo.create(user)

    async def update_user(self, user_id: str, data: UserUpdate) -> User:
        """Apply a partial update to an existing user.

        Only fields explicitly set (not ``None``) in *data* are written.
        """
        user = await self.get_by_id(user_id)  # raises NotFoundError
        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return user  # nothing to change
        return await self._repo.update(user, update_fields)

    async def deactivate_user(self, user_id: str) -> User:
        """Soft-delete a user by setting ``is_active = False``."""
        user = await self.get_by_id(user_id)
        return await self._repo.update(user, {"is_active": False})

    async def reactivate_user(self, user_id: str) -> User:
        """Re-enable a previously deactivated user."""
        user = await self.get_by_id(user_id)
        return await self._repo.update(user, {"is_active": True})

    async def record_login(self, user_id: str) -> User:
        """Update ``last_login`` to the current UTC timestamp."""
        user = await self.get_by_id(user_id)
        return await self._repo.update(
            user, {"last_login": datetime.now(timezone.utc)}
        )

    # ------------------------------------------------------------------ #
    # OAuth convenience
    # ------------------------------------------------------------------ #
    async def get_or_create_from_google(self, data: UserCreate) -> tuple[User, bool]:
        """Return an existing user or create a new one from Google data.

        Returns a ``(user, created)`` tuple where *created* is ``True`` when
        a new record was inserted.  On returning users the ``last_login`` and
        profile fields are updated automatically.
        """
        existing = await self._repo.get_by_google_id(data.google_id)
        if existing is not None:
            # Refresh profile data & bump last_login on every sign-in.
            await self._repo.update(
                existing,
                {
                    "name": data.name,
                    "email": data.email,
                    "profile_picture": data.profile_picture,
                    "last_login": datetime.now(timezone.utc),
                },
            )
            return existing, False

        user = await self.create_user(data)
        return user, True
