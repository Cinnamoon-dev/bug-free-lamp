from fastapi.responses import JSONResponse

from src.services import paginate
from src.infra.database.database import PgDatabase
from src.infra.database import retrieve_table_columns
from src.schemas.userSchema import UserAddSchema, UserEditSchema

class UserService:
    def __init__(self) -> None:
        self.table = "usuario"
        self.columns = retrieve_table_columns(self.table)
    
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