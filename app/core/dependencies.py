"""
app/core/dependencies.py
------------------------
FastAPI dependency providers (Depends-compatible callables).

Centralising dependencies here prevents circular imports and makes the
injection graph easy to reason about.
"""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import TokenError
from app.core.security import decode_token
from app.database.session import get_db_session

# Re-export for convenience so routers only need to import from here.
__all__ = [
    "get_settings",
    "get_session",
    "get_current_token_payload",
    "get_current_user_id",
    "get_weight_log_service",
    "get_measurement_session_service",
    "get_exercise_service",
    "get_exercise_log_service",
]

_bearer = HTTPBearer(auto_error=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an :class:`AsyncSession` for the current request lifecycle."""
    async for session in get_db_session():
        yield session


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Decode and return the JWT payload from the Authorization header.

    Raises HTTP 401 if the token is missing or invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(credentials.credentials)
    except (JWTError, TokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# TODO: Replace this stub with the real JWT-based implementation below
# once Google OAuth is fully implemented.
#
# async def get_current_user_id(
#     payload: dict = Depends(get_current_token_payload),
# ) -> str:
#     user_id: str | None = payload.get("sub")
#     if user_id is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token payload missing 'sub' claim",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user_id

# ── DEV-ONLY STUB ────────────────────────────────────────────────────────
_DEV_TEST_USER_ID = "00000000-0000-0000-0000-000000000001"


async def get_current_user_id() -> str:
    """Return a fixed test user ID for development.

    .. warning::
        This bypasses all authentication.  **Must** be replaced with the
        JWT-based version above before deploying to production.
    """
    return _DEV_TEST_USER_ID


# ---------------------------------------------------------------------------
# WeightLog
# ---------------------------------------------------------------------------
def get_weight_log_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`WeightLogRepository` bound to the request session."""
    from app.repositories.weight_log import WeightLogRepository

    return WeightLogRepository(session)


def get_weight_log_service(
    repo=Depends(get_weight_log_repository),
):
    """Provide a :class:`WeightLogService` with its repository injected."""
    from app.services.weight_log import WeightLogService

    return WeightLogService(repo)


# ---------------------------------------------------------------------------
# MeasurementSession
# ---------------------------------------------------------------------------
def get_measurement_session_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide a :class:`MeasurementSessionRepository` bound to the request session."""
    from app.repositories.measurement_session import MeasurementSessionRepository

    return MeasurementSessionRepository(session)


def get_measurement_session_service(
    repo=Depends(get_measurement_session_repository),
):
    """Provide a :class:`MeasurementSessionService` with its repository injected."""
    from app.services.measurement_session import MeasurementSessionService

    return MeasurementSessionService(repo)


# ---------------------------------------------------------------------------
# Exercise
# ---------------------------------------------------------------------------
def get_exercise_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide an :class:`ExerciseRepository` bound to the request session."""
    from app.repositories.exercise import ExerciseRepository

    return ExerciseRepository(session)


def get_exercise_service(
    repo=Depends(get_exercise_repository),
):
    """Provide an :class:`ExerciseService` with its repository injected."""
    from app.services.exercise import ExerciseService

    return ExerciseService(repo)


# ---------------------------------------------------------------------------
# ExerciseLog
# ---------------------------------------------------------------------------
def get_exercise_log_repository(
    session: AsyncSession = Depends(get_session),
):
    """Provide an :class:`ExerciseLogRepository` bound to the request session."""
    from app.repositories.exercise_log import ExerciseLogRepository

    return ExerciseLogRepository(session)


def get_exercise_log_service(
    repo=Depends(get_exercise_log_repository),
    exercise_service=Depends(get_exercise_service),
):
    """Provide an :class:`ExerciseLogService` with its repository injected."""
    from app.services.exercise_log import ExerciseLogService

    return ExerciseLogService(repo, exercise_service)
