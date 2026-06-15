"""
app/auth/router.py
------------------
Authentication endpoints – Google OAuth scaffold + token refresh.

These routes are *scaffolded only* – the user persistence / session creation
logic referenced by TODO comments will be implemented in the auth service once
business models exist.
"""

from __future__ import annotations

import secrets

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import RedirectResponse

from app.auth.oauth import (
    build_google_auth_url,
    exchange_code_for_tokens,
    get_google_user_info,
)
from app.core.config import get_settings
from app.schemas.common import MessageResponse

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(
    "/google/login",
    summary="Initiate Google OAuth flow",
    response_description="Redirect to Google consent screen",
)
async def google_login() -> RedirectResponse:
    """Redirect the browser to Google's OAuth consent screen.

    A random ``state`` token is generated for CSRF protection.
    In production this should be stored server-side (e.g. in Redis / a signed
    cookie) and verified on callback.
    """
    state = secrets.token_urlsafe(32)
    auth_url = build_google_auth_url(state=state)
    return RedirectResponse(url=auth_url, status_code=status.HTTP_302_FOUND)


@router.get(
    "/google/callback",
    summary="Google OAuth callback",
    response_model=MessageResponse,
)
async def google_callback(
    code: str = Query(..., description="Authorisation code from Google"),
    state: str | None = Query(None, description="State token for CSRF verification"),
    error: str | None = Query(None, description="Error returned by Google"),
) -> MessageResponse:
    """Handle the redirect from Google after user consent.

    Steps (TODO – implement once User model is available):
    1. Verify *state* against the value stored during ``/google/login``.
    2. Exchange *code* for access + id tokens.
    3. Fetch the user's profile from Google.
    4. Find or create the user in the database.
    5. Issue application-level access + refresh tokens.
    6. Return (or redirect with) the tokens.
    """
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth error: {error}",
        )

    # --- Step 2: token exchange -------------------------------------------
    try:
        token_data = await exchange_code_for_tokens(code)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to exchange authorisation code with Google.",
        ) from exc

    # --- Step 3: fetch profile -------------------------------------------
    try:
        user_info = await get_google_user_info(token_data["access_token"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to retrieve user profile from Google.",
        ) from exc

    # --- Steps 4-6: TODO --------------------------------------------------
    # user = await auth_service.find_or_create_google_user(user_info)
    # access_token  = create_access_token(subject=user.id)
    # refresh_token = create_refresh_token(subject=user.id)
    # return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    return MessageResponse(
        message="Google OAuth scaffold – user persistence not yet implemented.",
        detail={"google_sub": user_info.get("sub"), "email": user_info.get("email")},
    )
