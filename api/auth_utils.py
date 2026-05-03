"""Minimal JWT sign/verify using stdlib only (HS256)."""
import os, time, hmac, hashlib, base64, json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
_SECRET = os.getenv("JWT_SECRET", "change-me").encode()


def _b64url_enc(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_dec(s: str) -> bytes:
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)


def _sign(header: str, payload: str) -> str:
    return _b64url_enc(
        hmac.new(_SECRET, f"{header}.{payload}".encode(), hashlib.sha256).digest()
    )


def create_jwt(user: dict) -> str:
    header  = _b64url_enc(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64url_enc(json.dumps({
        "sub":        user["id"],
        "email":      user["email"],
        "name":       user.get("name") or "",
        "picture":    user.get("picture") or "",
        "theme_mode": user.get("theme_mode") or "light",
        "iat":        int(time.time()),
        "exp":        int(time.time()) + 86400 * 30,
    }).encode())
    return f"{header}.{payload}.{_sign(header, payload)}"


def verify_jwt(token: str) -> dict | None:
    try:
        header, payload, sig = token.split(".")
        if sig != _sign(header, payload):
            return None
        data = json.loads(_b64url_dec(payload))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None
