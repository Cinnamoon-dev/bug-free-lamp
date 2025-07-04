from typing import Any
from fastapi.responses import JSONResponse
from psycopg2.errors import UniqueViolation

from src.infra.database.database import PgDatabase
from src.schemas.userTypeSchema import UserTypeSchema


class UserTypeService:
    def __init__(self) -> None:
        self.table: str = "tipo_usuario"
        self.columns: list[str] = ["id", "nome"]

    def get_all(self) -> list[dict[str, Any]]:
        all_user_types = []

        with PgDatabase() as db:
            db.cursor.execute(f"SELECT id, nome FROM {self.table};")
            rows = db.cursor.fetchall()

            all_user_types = [{"id": row[0], "nome": row[1]} for row in rows]
        
        return all_user_types

    def add(self, user_type: UserTypeSchema) -> JSONResponse:
        # TODO
        # Make this generic
        # table_name, list_of_columns, tuple_with_fields (in the list_of_columns order)

        try:
            with PgDatabase() as db:
                db.cursor.execute(f"INSERT INTO {self.table} (nome) VALUES (%s)", (user_type.nome,))
                db.connection.commit()
        except UniqueViolation:
            return JSONResponse(status_code=400, content={"error": True, "message": f"Tipo de usuário com o nome {user_type.nome} já existe"})
        except Exception:
            return JSONResponse(status_code=500, content={"error": True, "message": "Database error"})
        
        return JSONResponse(status_code=200, content={"error": False, "message": f"Tipo de usuário {user_type.nome} adicionado com sucesso."})
        