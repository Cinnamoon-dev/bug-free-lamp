from typing import Any
from fastapi.responses import JSONResponse
from psycopg2.errors import UniqueViolation

from src.infra.database.database import PgDatabase
from src.schemas.userTypeSchema import UserTypeSchema


class UserTypeService:
    def __init__(self) -> None:
        self.table: str = "tipo_usuario"
        self.columns: list[str] = ["id", "nome"]

    def all(self) -> list[dict[str, Any]]:
        # TODO
        # pagination
        all_user_types = []

        with PgDatabase() as db:
            db.cursor.execute(f"SELECT id, nome FROM {self.table};")
            rows = db.cursor.fetchall()

            all_user_types = [{"id": row[0], "nome": row[1]} for row in rows]
        
        return all_user_types

    def view(self, user_type_id: int) -> JSONResponse:
        user_type = None

        with PgDatabase() as db:
            db.cursor.execute(f"SELECT id, nome FROM {self.table} WHERE id = %s", (user_type_id,))
            row = db.cursor.fetchone()

            if row is None:
                return JSONResponse(status_code=404, content={"error": True, "message": "Tipo de usuário não encontrado"})
        
        user_type = {"id": row[0], "nome": row[1]}
        return JSONResponse(status_code=200, content={"error": False, "data": user_type})

    def add(self, user_type: UserTypeSchema) -> JSONResponse:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"INSERT INTO {self.table} (nome) VALUES (%s)", (user_type.nome,))
                db.connection.commit()
        except UniqueViolation as e:
            return JSONResponse(status_code=400, content={"error": True, "message": str(e)})
        except Exception:
            return JSONResponse(status_code=500, content={"error": True, "message": "Database error"})
        
        return JSONResponse(status_code=200, content={"error": False, "message": f"Tipo de usuário {user_type.nome} adicionado com sucesso."})
        
    def edit(self, user_type_id: int, user_type: UserTypeSchema) -> JSONResponse:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"UPDATE {self.table} SET nome = %s WHERE id = %s", (user_type.nome, user_type_id))
                db.connection.commit()
        except UniqueViolation as e:
            return JSONResponse(status_code=400, content={"error": True, "message": str(e)})
        except Exception:
            return JSONResponse(status_code=500, content={"error": True, "message": "Database error"})

        return JSONResponse(status_code=200, content={"error": False, "message": f"Tipo de usuário com id {user_type_id} editado com sucesso."})
    
    def delete(self, user_type_id: int):
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (user_type_id,))
        except Exception:
            return JSONResponse(status_code=500, content={"error": True, "message": "Database error"})

        return JSONResponse(status_code=200, content={"error": False, "message": f"Tipo de usuário com id {user_type_id} deletado com sucesso."})