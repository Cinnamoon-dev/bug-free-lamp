from functools import reduce
from typing import Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from psycopg2.errors import UniqueViolation
from fastapi.datastructures import QueryParams

from src.infra.database.database import PgDatabase
from src.services import paginate, fields_to_update
from src.infra.database import retrieve_table_columns
from src.schemas.userTypeSchema import UserTypeSchema
from src.infra.database.serializers import line_to_dict


class UserTypeService:
    def __init__(self) -> None:
        self.table: str = "tipo_usuario"
        self.columns: list[str] = retrieve_table_columns(self.table)
        try:
            self.all_columns = reduce(lambda acc, elem: acc + ", " + str(elem), self.columns)
        except Exception:
            self.all_columns = "*"

    def all(self, query_params: QueryParams) -> dict[str, Any]:
        query = f"SELECT {self.all_columns} FROM {self.table}"
        page = int(query_params.get("page", 1))
        rows_per_page = int(query_params.get("rows_per_page", 10))
        sort = query_params.get("sort_by", None)

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

    def view(self, user_type_id: int) -> dict[str, Any]:
        user_type = None

        try:
            with PgDatabase() as db:
                db.cursor.execute(f"SELECT {self.all_columns} FROM {self.table} WHERE id = %s", (user_type_id,))
                row = db.cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail={"error": True, "message": "Tipo de usuário não encontrado"})
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})
        
        user_type = line_to_dict(row, self.columns)
        return user_type

    def add(self, user_type: UserTypeSchema) -> dict[str, Any]:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"INSERT INTO {self.table} (nome) VALUES (%s) RETURNING id", (user_type.nome,))
                raw_id = db.cursor.fetchone()

                if raw_id is None:
                    raise HTTPException(status_code=500, detail={"error": True, "message": "Não foi possível inserir o tipo de usuário."})

                inserted_id = raw_id[0]
                db.connection.commit()
        except UniqueViolation as e:
            raise HTTPException(status_code=400, detail={"error": True, "message": str(e)})
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})
        
        return {"error": False, "message": f"Tipo de usuário {user_type.nome} adicionado com sucesso.", "id": inserted_id}
        
    def edit(self, user_type_id: int, user_type: UserTypeSchema) -> dict[str, Any]:
        user_type_dict = user_type.model_dump(exclude_none=True)
        if not user_type_dict:
            raise HTTPException(status_code=200, detail={"error": False, "message": f"Tipo de usuário com id {user_type_id} editado com sucesso."})

        set_fields, set_values = fields_to_update(user_type_dict)
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"UPDATE {self.table} SET {set_fields} WHERE id = %s", set_values + (user_type_id,))
                db.connection.commit()
        except UniqueViolation as e:
            raise HTTPException(status_code=400, detail={"error": True, "message": str(e)})
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})

        return {"error": False, "message": f"Tipo de usuário com id {user_type_id} editado com sucesso."}
    
    def delete(self, user_type_id: int) -> dict[str, Any]:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (user_type_id,))
                db.connection.commit()
        except Exception:
            raise HTTPException(status_code=500, detail={"error": True, "message": "Database error"})

        return {"error": False, "message": f"Tipo de usuário com id {user_type_id} deletado com sucesso."}