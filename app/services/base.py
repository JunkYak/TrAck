"""
app/services/base.py
--------------------
Abstract service base class.

Every service receives its dependencies (repositories, etc.) through
constructor injection, keeping them independently testable and decoupled
from the framework (Dependency Inversion Principle).
"""

from __future__ import annotations

from abc import ABC


class BaseService(ABC):
    """Marker base for all service classes.

    Concrete services should declare their repository/dependency parameters
    in ``__init__`` and accept them via FastAPI's ``Depends`` mechanism or
    manual injection in tests.

    Example::

        class UserService(BaseService):
            def __init__(self, user_repo: UserRepository) -> None:
                self._repo = user_repo

            async def get_user(self, user_id: int) -> User:
                user = await self._repo.get_by_id(user_id)
                if user is None:
                    raise NotFoundError(f"User {user_id} not found")
                return user
    """
