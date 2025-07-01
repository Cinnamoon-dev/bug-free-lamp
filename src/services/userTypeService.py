from typing import Any

from src.infra.database.database import PgDatabase
from src.schemas.userTypeSchema import UserTypeSchema


class UserTypeService:
    def __init__(self) -> None:
        self.table = "tipo_usuario"
        self.columns = ["id", "nome"]

    def get_all(self) -> list[dict[str, Any]]:
        all_user_types = []

        with PgDatabase() as db:
            db.cursor.execute(f"SELECT id, nome FROM {self.table};")
            rows = db.cursor.fetchall()

            all_user_types = [{"id": row[0], "nome": row[1]} for row in rows]
        
        return all_user_types

    def add(self, user_type: UserTypeSchema):
        return