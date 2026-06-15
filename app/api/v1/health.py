"""
app/api/v1/health.py
--------------------
Health-check endpoint.

Returns application metadata and a lightweight database connectivity probe.
Kubernetes liveness / readiness probes, load-balancers, and uptime monitors
can all target ``GET /health``.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from app.core.config import get_settings
from app.core.dependencies import get_session
from app.schemas.common import HealthResponse

settings = get_settings()
router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description=(
        "Returns the service status, version, environment, "
        "and a lightweight database connectivity probe."
    ),
)
async def health_check(
    session: AsyncSession = Depends(get_session),
) -> HealthResponse:
    """Verify the application is running and can reach the database."""
    db_status = "ok"
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        db_status = "unreachable"

    return HealthResponse(
        status="ok",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        database=db_status,
    )
