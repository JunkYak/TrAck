"""
app/services/auth.py
--------------------
Service layer for authentication. Handles the creation and lookup of Users via OAuth.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from app.models.user import User
from app.repositories.user import UserRepository

class AuthService:
    """Business logic for authentication and user sessions."""

    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def find_or_create_google_user(self, user_info: Dict[str, Any]) -> User:
        """
        Takes a Google OAuth user profile, looks up the user by `google_id`.
        If the user exists, updates their last_login.
        If they do not exist, creates a new User record.
        """
        google_id = user_info.get("sub")
        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture")

        if not google_id or not email or not name:
            raise ValueError("Google profile is missing required fields (sub, email, name)")

        user = await self._repo.get_by_google_id(google_id)
        now = datetime.now(timezone.utc)

        if user:
            # Update last login
            user.last_login = now
            return await self._repo.update(user, {"last_login": now})
        
        # User doesn't exist, create them
        new_user = User(
            google_id=google_id,
            email=email,
            name=name,
            profile_picture=picture,
            last_login=now
        )
        return await self._repo.create(new_user)
