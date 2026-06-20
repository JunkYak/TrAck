"""
app/core/config.py
------------------
Centralised application settings loaded from environment variables / .env file.
Uses pydantic-settings so every field is typed and validated at startup.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All application-level configuration lives here.

    Values are read from environment variables first, then from a .env file.
    Prefix fields with their logical group so the source is obvious at a
    glance (e.g. ``DB_URL``, ``JWT_SECRET``).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------ #
    # Application
    # ------------------------------------------------------------------ #
    APP_NAME: str = "Track"
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    APP_VERSION: str = "0.1.0"
    SECRET_KEY: str = "change-me-to-a-long-random-secret-key"

    # ------------------------------------------------------------------ #
    # Server
    # ------------------------------------------------------------------ #
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ------------------------------------------------------------------ #
    # Database
    # ------------------------------------------------------------------ #
    DATABASE_URL: str = "sqlite+aiosqlite:///./track.db"

    # ------------------------------------------------------------------ #
    # JWT
    # ------------------------------------------------------------------ #
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200 # 30 Days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ------------------------------------------------------------------ #
    # Application / Frontend
    # ------------------------------------------------------------------ #
    FRONTEND_URL: str = "http://localhost:5173"

    # ------------------------------------------------------------------ #
    # Google OAuth (scaffold – values filled via .env)
    # ------------------------------------------------------------------ #
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    # ------------------------------------------------------------------ #
    # CORS
    # ------------------------------------------------------------------ #
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def _parse_origins(cls, value: str | List[str]) -> List[str]:
        """Accept a comma-separated string or a list."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    # ------------------------------------------------------------------ #
    # Derived helpers
    # ------------------------------------------------------------------ #
    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton of :class:`Settings`.

    Using ``lru_cache`` ensures the .env file is parsed exactly once and the
    same object is returned for every dependency injection call.
    """
    return Settings()
