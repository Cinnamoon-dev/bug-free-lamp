from datetime import timedelta
from fastapi import APIRouter, HTTPException, Header, Request, Response

from src.infra.database.database import PgDatabase
from src.services.userService import UserService
from ._helpers import user_dependency, form_auth_dependency
from src.infra.security.hashing import (
    ALGORITHM,
    create_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    JWT_ACCESS_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
    bcrypt_context,
    decode_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(form_data: form_auth_dependency):
    email = form_data.username.lower()
    user = UserService(PgDatabase()).view_by_email(email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail={"message": "Email or password incorrect.", "error": True},
        )

    if not bcrypt_context.verify(form_data.password, user["senha"]):
        raise HTTPException(
            status_code=401,
            detail={"message": "Email or password incorrect.", "error": True},
        )

    access_token = create_token(
        user["id"],
        JWT_ACCESS_SECRET_KEY,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        user["id"], JWT_REFRESH_SECRET_KEY, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.post("/login/cookie")
def login_cookie(form_data: form_auth_dependency, response: Response):
    email = form_data.username.lower()
    user = UserService(PgDatabase()).view_by_email(email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail={"message": "Email or password incorrect.", "error": True},
        )

    if not bcrypt_context.verify(form_data.password, user["senha"]):
        raise HTTPException(
            status_code=401,
            detail={"message": "Email or password incorrect.", "error": True},
        )

    access_token = create_token(
        user["id"],
        JWT_ACCESS_SECRET_KEY,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        user["id"], JWT_REFRESH_SECRET_KEY, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    response.set_cookie(
        "access_token",
        access_token
    )

    response.set_cookie(
        "refresh_token",
        refresh_token
    )

    response.set_cookie(
        "token_type",
        "Bearer"
    )

    return {"message": "Login successfull"}


@router.post("/refresh/cookie")
def refresh_cookie(
    response: Response,
    refresh_token: str = Header(..., alias="refresh_token")
):
    payload = decode_token(refresh_token, JWT_REFRESH_SECRET_KEY, [ALGORITHM])
    user_id = int(payload["sub"])

    user = UserService(PgDatabase()).view(user_id)
    if not user:
        raise HTTPException(
            status_code=401, detail={"message": "User not found", "error": True}
        )

    new_access_token = create_token(
        payload["sub"],
        JWT_ACCESS_SECRET_KEY,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = create_token(
        payload["sub"],
        JWT_REFRESH_SECRET_KEY,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    response.set_cookie(
        "access_token",
        new_access_token
    )

    response.set_cookie(
        "refresh_token",
        new_refresh_token
    )

    response.set_cookie(
        "token_type",
        "Bearer"
    )

    return {"message": "Token refreshed successfully"}


@router.post("/refresh")
def refresh(refresh_token: str = Header(..., alias="X-Refresh-Token")):
    payload = decode_token(refresh_token, JWT_REFRESH_SECRET_KEY, [ALGORITHM])
    user_id = int(payload["sub"])

    user = UserService(PgDatabase()).view(user_id)
    if not user:
        raise HTTPException(
            status_code=401, detail={"message": "User not found", "error": True}
        )

    new_access_token = create_token(
        payload["sub"],
        JWT_ACCESS_SECRET_KEY,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = create_token(
        payload["sub"],
        JWT_REFRESH_SECRET_KEY,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "Bearer",
    }


@router.get("/me")
def me(request: Request, user: user_dependency, show_fk_id: int | None = 1):
    if show_fk_id == 0:
        return UserService(PgDatabase()).view_controller(user["id"], request.query_params)

    return user
