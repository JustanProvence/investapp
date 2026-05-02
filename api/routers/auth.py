from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services import users_store
from dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str


@router.post("/login")
def login(body: LoginRequest):
    user = users_store.get_by_email(body.email.strip().lower())
    if not user:
        raise HTTPException(status_code=401, detail="Email not recognised")
    return user


class PreferencesRequest(BaseModel):
    theme_mode: str


@router.patch("/preferences")
def update_preferences(body: PreferencesRequest, user: dict = Depends(get_current_user)):
    users_store.set_theme_mode(user["id"], body.theme_mode)
    return {"ok": True}
