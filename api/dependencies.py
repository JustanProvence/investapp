from fastapi import Header, HTTPException
from services import users_store


def get_current_user(x_user_id: str | None = Header(default=None)) -> dict:
    """Reads the logged-in user from the X-User-Id request header.
    Replaced by JWT Bearer token verification when Google OAuth is added."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = users_store.get_by_id(x_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
