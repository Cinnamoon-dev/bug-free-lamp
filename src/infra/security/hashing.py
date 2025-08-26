import os
import jwt
import json
from fastapi import Depends, HTTPException
from typing import Annotated, Any
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

from src.services.userService import UserService


JWT_ACCESS_SECRET_KEY = os.getenv("JWT_ACCESS_SECRET_KEY", "5978c7af950f2a6097b4f07701b388a57abea6c4bbc36f09a7677306653e7796")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "8f1b0cfb3694d16b60beccac61b2a40bec9e5fedbf59d1fed1c0cbb050f37236")
ALGORITHM = "HS512"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

bcrypt_context = CryptContext(
    schemes=["sha512_crypt"],
    deprecated="auto",
    sha512_crypt__default_rounds=5000
)

def create_token(user_id: int, secret_key: str, expires_delta: timedelta) -> str:
    to_encode: dict[str, Any] = {"sub": user_id}
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
token_dependency = Annotated[str, Depends(oauth2_bearer)]


def get_current_user(token: token_dependency) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(token, JWT_ACCESS_SECRET_KEY, ALGORITHM)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuário não autorizado")
        
        user = UserService().view(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except:
        raise HTTPException(status_code=500, detail="Erro ao autenticar usuário")
    
    return json.loads(user.body)

user_dependency = Annotated[dict[str, Any], Depends(get_current_user)]