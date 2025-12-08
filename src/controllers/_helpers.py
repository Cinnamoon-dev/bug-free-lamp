from typing import Annotated, Any
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.services.userService import UserService
from src.infra.database.database import PgDatabase
from src.infra.security.hashing import ALGORITHM, JWT_ACCESS_SECRET_KEY, decode_token

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)
token_dependency = Annotated[str | None, Depends(oauth2_bearer)]


def get_token_from_cookie(request: Request) -> str:
    auth_jwt = request.cookies.get("access_token")

    if auth_jwt is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    return auth_jwt

def get_current_user(token: token_dependency, request: Request) -> dict[str, Any]:
    if token is None:
        token = get_token_from_cookie(request)

    payload: dict[str, Any] = decode_token(token, JWT_ACCESS_SECRET_KEY, [ALGORITHM])
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Usuário não autorizado")

    user = UserService(PgDatabase()).view(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


user_dependency = Annotated[dict[str, Any], Depends(get_current_user)]
form_auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, user: user_dependency):
        controller, action = self.required_permission.split("-")
        user_type_id = user["tipo_usuario_id"]

        query = """
            SELECT regras.acao, regras.permitir, controllers.nome, tipo_usuario.nome 
            FROM regras
            JOIN controllers ON controllers.id = regras.controller_id
            JOIN tipo_usuario ON tipo_usuario.id = regras.tipo_usuario_id
            WHERE tipo_usuario.id = %s AND regras.permitir = True AND controllers.nome = %s AND regras.acao = %s
        """

        with PgDatabase() as db:
            db.cursor.execute(query, (user_type_id, controller, action))
            row = db.cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=403,
                    detail={"message": "Usuário não autorizado", "error": True},
                )
