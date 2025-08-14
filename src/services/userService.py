from fastapi.responses import JSONResponse
from fastapi.datastructures import QueryParams

from src.infra.database.serializers import line_to_dict
from src.services import paginate
from src.infra.database.database import PgDatabase
from src.infra.database import retrieve_table_columns
from src.schemas.userSchema import UserAddSchema, UserEditSchema

class UserService:
    def __init__(self) -> None:
        self.table = "usuario"
        self.columns = retrieve_table_columns(self.table)

    def all(self, query_params: QueryParams) -> JSONResponse:
        query = f"SELECT id, email, senha, tipo_id FROM {self.table}"
        page = int(query_params.get("page", 1))
        rows_per_page = int(query_params.get("rows_per_page", 10))
        sort = query_params.get("sort_by", None)

        if sort is not None:
            sort_column, sort_order = sort.split(",")

            if sort_column not in self.columns:
                return JSONResponse({"error": True, "message": f"Coluna {sort_column} não identificada"}, 400)

            if sort_order.lower() not in ["asc", "desc"]:
                return JSONResponse({"error": True, "message": f"Direção de ordenação {sort_order} inválida, deve ser 'asc' ou 'desc'"}, 400)
        
        output = paginate(query, page, rows_per_page, sort) 
        return JSONResponse(output, 200)

    def view(self, user_id: int) -> JSONResponse:
        user = None

        with PgDatabase() as db:
            db.cursor.execute(f"SELECT id, email, senha, tipo_id FROM {self.table} WHERE id = %s", (user_id,))
            row = db.cursor.fetchone()

            if row is None:
                return JSONResponse(status_code=404, content={"error": True, "message": "Usuário não encontrado"})
        
        user = line_to_dict(row, self.columns)
        return JSONResponse(status_code=200, content={"error": False, "data": user})
    
    def add(self, user: UserAddSchema) -> JSONResponse:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"INSERT INTO {self.table} (email, senha, tipo_id) VALUES (%s, %s, %s) RETURNING id", (user.email, user.senha, user.tipo_id))
                raw_id = db.cursor.fetchone()

                if raw_id is None:
                    return JSONResponse(status_code=500, content={"error": True, "message": f"Não foi possível inserir o usuário {user.email}."})

                inserted_id = raw_id[0]
                db.connection.commit()
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
        
        return JSONResponse(status_code=200, content={"error": False, "message": f"Usuário {user.email} adicionado com sucesso.", "id": inserted_id})

    def edit(self, user_id: int, user: UserEditSchema) -> JSONResponse:
        try:
            with PgDatabase() as db:
                # TODO
                # Criar método para escolher os campos que vao para o SET
                #db.cursor.execute(f"UPDATE {self.table} SET nome = %s WHERE id = %s", (user_type.nome, user_type_id))
                db.connection.commit()
        except Exception:
            return JSONResponse(status_code=500, content={"error": True, "message": "Database error"})

        return JSONResponse(status_code=200, content={"error": False, "message": f"Usuário com id {user_id} editado com sucesso."})

    def delete(self, user_id: int) -> JSONResponse:
        try:
            with PgDatabase() as db:
                db.cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (user_id,))
                db.connection.commit()
        except Exception:
            return JSONResponse(status_code=500, content={"error": True, "message": "Database error"})

        return JSONResponse(status_code=200, content={"error": False, "message": f"Usuário com id {user_id} deletado com sucesso."})