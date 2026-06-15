"""
app/auth/oauth.py
-----------------
Google OAuth 2.0 scaffold.

This module provides the URL-building and token-exchange helpers for the
Google OAuth flow.  It is intentionally **scaffolded only** – the endpoints
are wired but the user-creation/session logic is left for the business layer.

References
~~~~~~~~~~
* https://developers.google.com/identity/protocols/oauth2/web-server
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from app.core.config import get_settings

settings = get_settings()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

SCOPES = ["openid", "email", "profile"]


def build_google_auth_url(state: str | None = None) -> str:
    """Return the Google consent-screen URL the client should redirect to.

    Args:
        state: Optional opaque value for CSRF protection.  Pass a
               cryptographically random string and verify it on callback.
    """
    params: dict[str, Any] = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    if state:
        params["state"] = state

    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


async def exchange_code_for_tokens(code: str) -> dict[str, Any]:
    """Exchange an authorisation *code* for Google access/id tokens.

    Args:
        code: The ``code`` query parameter received on the OAuth callback.

    Returns:
        The raw JSON response from Google's token endpoint, which includes
        ``access_token``, ``id_token``, ``expires_in``, etc.

    Raises:
        httpx.HTTPStatusError: If Google returns a non-2xx response.
    """
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TOKEN_URL, data=payload)
        response.raise_for_status()
        return response.json()


async def get_google_user_info(access_token: str) -> dict[str, Any]:
    """Fetch the authenticated user's profile from Google.

    Args:
        access_token: A valid Google OAuth access token.

    Returns:
        Dict with keys ``sub``, ``email``, ``name``, ``picture``, etc.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        response.raise_for_status()
        return response.json()
