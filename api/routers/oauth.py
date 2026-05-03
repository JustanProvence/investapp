import os
from pathlib import Path
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from services import users_store
from auth_utils import create_jwt

load_dotenv(Path(__file__).parents[2] / ".env")

_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
_REDIRECT_URI  = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
_FLET_BASE     = os.getenv("FLET_BASE_URL", "http://localhost:8550")

router = APIRouter(prefix="/auth", tags=["oauth"])


@router.get("/google/authorize")
def google_authorize():
    params = urlencode({
        "client_id":     _CLIENT_ID,
        "redirect_uri":  _REDIRECT_URI,
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "offline",
        "prompt":        "select_account",
    })
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{params}")


@router.get("/google/callback")
async def google_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code":          code,
                "client_id":     _CLIENT_ID,
                "client_secret": _CLIENT_SECRET,
                "redirect_uri":  _REDIRECT_URI,
                "grant_type":    "authorization_code",
            },
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return RedirectResponse(f"{_FLET_BASE}/?error=auth_failed")

        info_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        info = info_resp.json()

    user = users_store.upsert(
        user_id=info["id"],
        email=info["email"],
        name=info.get("name", ""),
        picture=info.get("picture"),
    )
    token = create_jwt(user)
    return RedirectResponse(f"{_FLET_BASE}/auth/callback/{token}")
