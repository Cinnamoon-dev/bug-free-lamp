from typing import Any
from functools import reduce
from fastapi import HTTPException
from fastapi.datastructures import QueryParams

from src.infra.database.database import PgDatabase
from src.services import paginate, fields_to_update
from src.infra.security.hashing import bcrypt_context
from src.infra.database import retrieve_table_columns
from src.infra.database.serializers import line_to_dict
from src.schemas.userSchema import UserAddSchema, UserEditSchema

class UserService:
    def __init__(self) -> None:
        self.table = "usuario"
        self.columns = retrieve_table_columns(self.table)
        try:
            self.all_columns = reduce(lambda acc, elem: acc + ", " + str(elem), self.columns)
        except Exception:
            self.all_columns = "*"

    def all(self, query_params: QueryParams) -> dict[str, Any]:
        show_fk_id = bool(int(query_params.get("show_fk_id", 1)))
        page = int(query_params.get("page", 1))
        rows_per_page = int(query_params.get("rows_per_page", 10))
        sort = query_params.get("sort_by", None)

        if show_fk_id:
            query = f"SELECT {self.all_columns} FROM {self.table}"
        else:
            query = f"SELECT u.id, u.email, u.senha, tu.nome AS tipo_usuario FROM {self.table} AS u INNER JOIN tipo_usuario AS tu ON u.tipo_usuario_id=tu.id"

        if sort is not None:
            try:
                sort_column, sort_order = sort.split(",")
            except Exception:
                raise HTTPException(status_code=422, detail={"error": True, "message": f"Coluna e direção {sort} não separada corretamente por ','"})

            if sort_column not in self.columns:
                raise HTTPException(status_code=422, detail={"error": True, "message": f"Coluna {sort_column} não identificada"})

            if sort_order.lower() not in ["asc", "desc"]:
                raise HTTPException(status_code=422, detail={"error": True, "message": f"Direção de ordenação {sort_order} inválida, deve ser 'asc' ou 'desc'"})
        
        output = paginate(query, page, rows_per_page, sort) 
        return output

    def view(self, user_id: int) -> dict[str, Any]:
        user = None

        try:
            with PgDatabase() as db:
                db.cursor.execute(f"SELECT {self.all_columns} FROM {self.table} WHERE id = %s", (user_id,))
                row = db.cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail={"error": True, "message": "Usuário não encontrado"})
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})
        
        user = line_to_dict(row, self.columns)
        return user
    

    def view_by_email(self, email: str) -> dict[str, Any]:
        user = None

        try:
            with PgDatabase() as db:
                db.cursor.execute(f"SELECT {self.all_columns} FROM {self.table} WHERE email = %s", (email,))
                row = db.cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail={"error": True, "message": "Usuário não encontrado"})
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})
        
        user = line_to_dict(row, self.columns)
        return user

    def add(self, user: UserAddSchema) -> dict[str, Any]:
        senha = bcrypt_context.hash(user.senha)
 
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"INSERT INTO {self.table} (email, senha, tipo_usuario_id) VALUES (%s, %s, %s) RETURNING id", (user.email.lower(), senha, user.tipo_usuario_id))
                raw_id = db.cursor.fetchone()

                if raw_id is None:
                    raise HTTPException(status_code=500, detail={"error": True, "message": f"Não foi possível inserir o usuário {user.email}."})

                inserted_id = raw_id[0]
                db.connection.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})
        
        return {"error": False, "message": f"Usuário {user.email} adicionado com sucesso.", "id": inserted_id}

    def edit(self, user_id: int, user: UserEditSchema) -> dict[str, Any]:
        user_dict = user.model_dump(exclude_none=True)
        if not user_dict:
            raise HTTPException(status_code=200, detail={"error": False, "message": f"Usuário com id {user_id} editado com sucesso."})

        set_fields, set_values = fields_to_update(user_dict)
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"UPDATE {self.table} SET {set_fields} WHERE id = %s", set_values + (user_id,))
                db.connection.commit()
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})

        return {"error": False, "message": f"Usuário com id {user_id} editado com sucesso."}

    def delete(self, user_id: int) -> dict[str, Any]:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (user_id,))
                db.connection.commit()
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})

        return {"error": False, "message": f"Usuário com id {user_id} deletado com sucesso."}