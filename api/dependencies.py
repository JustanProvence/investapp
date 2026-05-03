from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services import users_store
from auth_utils import verify_jwt

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    x_user_id: str | None = Header(default=None),
    credentials: HTTPAuthorizationCredentials | None = Security(_bearer),
) -> dict:
    # JWT Bearer token (Google OAuth path)
    if credentials:
        payload = verify_jwt(credentials.credentials)
        if payload:
            user = users_store.get_by_id(payload["sub"])
            if user:
                return user

    # X-User-Id header (dev / email login path)
    if x_user_id:
        user = users_store.get_by_id(x_user_id)
        if user:
            return user

    raise HTTPException(status_code=401, detail="Not authenticated")
