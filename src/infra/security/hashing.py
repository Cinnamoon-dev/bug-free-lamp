import os
import jwt
from typing import Any
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


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
    to_encode: dict[str, Any] = {"sub": str(user_id)}
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(jwt_token: str, secret_key: str | bytes, algorithms: list[str]) -> dict[str, Any]:
    try:
        payload = jwt.decode(jwt_token, secret_key, algorithms)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Erro ao autenticar usuário")
