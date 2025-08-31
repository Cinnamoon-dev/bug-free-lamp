from datetime import timedelta
from fastapi import APIRouter, HTTPException, Header

from src.services.userService import UserService
from ._helpers import user_dependency, form_auth_dependency
from src.infra.security.hashing import ALGORITHM, create_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, JWT_ACCESS_SECRET_KEY, JWT_REFRESH_SECRET_KEY, bcrypt_context, decode_token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: form_auth_dependency):
    email = form_data.username.lower()
    user = UserService().view_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail={"message": "Email or password incorrect.", "error": True}) 

    if not bcrypt_context.verify(form_data.password, user["senha"]):
        raise HTTPException(status_code=401, detail={"message": "Email or password incorrect.", "error": True})

    access_token = create_token(user["id"], JWT_ACCESS_SECRET_KEY, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(user["id"], JWT_REFRESH_SECRET_KEY, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@router.post("/refresh")
def refresh(refresh_token: str = Header(..., alias="X-Refresh-Token")):
    payload = decode_token(refresh_token, JWT_REFRESH_SECRET_KEY, [ALGORITHM])
    user_id = int(payload["sub"])

    user = UserService().view(user_id)
    if not user:
        raise HTTPException(status_code=401, detail={"message": "User not found", "error": True})

    new_access_token = create_token(payload["sub"], JWT_ACCESS_SECRET_KEY, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": new_access_token, "error": False}

@router.get("/me")
def me(user: user_dependency):
    return user