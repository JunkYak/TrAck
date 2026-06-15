"""
app/main.py
-----------
FastAPI application factory.

The ``create_app`` factory pattern keeps the application object easy to
import in tests (each test gets a fresh app instance) and makes it simple
to apply environment-specific configuration without global mutable state.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.auth.router import router as auth_router
from app.core.config import get_settings
from app.core.exceptions import (
    AlreadyExistsError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    TokenError,
    TrackBaseException,
    ValidationError,
)

settings = get_settings()


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup / shutdown logic.

    Startup:
        * (Placeholder) warm caches, verify external services, etc.
    Shutdown:
        * Dispose of the SQLAlchemy connection pool cleanly.
    """
    # -- startup --
    from app.database.session import engine  # imported here to avoid circular init

    yield

    # -- shutdown --
    await engine.dispose()


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
def create_app() -> FastAPI:
    """Construct and configure the FastAPI application."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Track – production-ready FastAPI backend.\n\n"
            "Built with SQLAlchemy (async), Alembic, Repository & Service patterns."
        ),
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------ #
    # Middleware
    # ------------------------------------------------------------------ #
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------ #
    # Exception handlers
    # ------------------------------------------------------------------ #
    _register_exception_handlers(app)

    # ------------------------------------------------------------------ #
    # Routers
    # ------------------------------------------------------------------ #
    app.include_router(api_v1_router)
    app.include_router(auth_router)

    return app


# ---------------------------------------------------------------------------
# Exception handler registration
# ---------------------------------------------------------------------------
def _register_exception_handlers(app: FastAPI) -> None:
    """Map domain exceptions to HTTP responses.

    Keeping this out of the exception classes themselves preserves SRP –
    domain exceptions have no knowledge of HTTP.
    """

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(
        request: Request, exc: AlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_handler(
        request: Request, exc: AuthorizationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.message},
        )

    @app.exception_handler(TokenError)
    async def token_error_handler(
        request: Request, exc: TokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.message},
        )

    @app.exception_handler(TrackBaseException)
    async def generic_domain_handler(
        request: Request, exc: TrackBaseException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )


# ---------------------------------------------------------------------------
# ASGI entry-point
# ---------------------------------------------------------------------------
app: FastAPI = create_app()
