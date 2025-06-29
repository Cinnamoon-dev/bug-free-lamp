import os
from src.infra.database.database import PgDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def populate() -> None:
    def insert(filePath: str) -> None:
        sql_file = open(BASE_DIR + filePath, "r")
        sql = sql_file.read()
        lines = sql.split(";")

        with PgDatabase() as db:
            for line in lines:
                print(line)
                if line.strip():
                    db.cursor.execute(line)
            
            db.connection.commit()

    insert("/scripts/tables.sql")

if __name__ == "__main__":
    populate()