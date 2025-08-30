import jwt
from typing import Annotated, Any
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.services.userService import UserService
from src.infra.security.hashing import ALGORITHM, JWT_ACCESS_SECRET_KEY, decode_token

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
token_dependency = Annotated[str, Depends(oauth2_bearer)]

def get_current_user(token: token_dependency) -> dict[str, Any]:
    payload: dict[str, Any] = decode_token(token, JWT_ACCESS_SECRET_KEY, [ALGORITHM])
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Usuário não autorizado")
    
    user = UserService().view(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return user

user_dependency = Annotated[dict[str, Any], Depends(get_current_user)]
form_auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]