import math
from typing import Any

from src.infra.database.database import PgDatabase
from src.infra.database.serializers import lines_to_dict


def paginate(
    table_name: str, 
    columns: list[str], 
    page: int,
    rows_per_page: int,
    sort: str | None
) -> dict[str, Any]:
    # TODO
    # Refactor: talvez receber a query e só adicionar o LIMIT, OFFSET E ORDER BY no final
    # para poder mexer com qualquer query, como as que tem JOIN e etc
    if sort is not None:
        sort_column, sort_order = sort.split(",")

        if sort_column not in columns:
            raise ValueError("Coluna não identificada")
        
        if sort_order.lower() not in ["asc", "desc"]:
            raise ValueError("Direção de ordenação não encontrada")

    if page < 1:
        page = 1
    
    if rows_per_page < 1:
        rows_per_page = 10
    
    prev_page = page - 1
    if prev_page < 1:
        prev_page = None

    next_page = page + 1

    offset = (page - 1) * rows_per_page
    columns_string = str(columns).strip("[]").replace("'", "")

    data = []

    # TODO
    # Tratar exceptions aqui
    with PgDatabase() as db:
        db.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        raw_count = db.cursor.fetchone()

        if raw_count is None:
            return {"error": True, "message": "Não foi possível fazer a query"}
        
        itens_count = raw_count[0]

        if sort:
            sort_column, sort_order = sort.split(",")
            db.cursor.execute(f"SELECT {columns_string} FROM {table_name} ORDER BY {sort_column} {sort_order} LIMIT %s OFFSET %s", (rows_per_page, offset))
        else:
            db.cursor.execute(f"SELECT {columns_string} FROM {table_name} LIMIT %s OFFSET %s", (rows_per_page, offset))

        lines = db.cursor.fetchall()
        data = lines_to_dict(lines, columns)

    pages_count = math.ceil(itens_count / rows_per_page)
    
    if pages_count in [0, 1]:
        next_page = None

    return {
        "itens": data,
        "pagination": {
            "pages_count": pages_count,
            "itens_count": itens_count,
            "itens_per_page": rows_per_page,
            "prev": prev_page,
            "next": next_page,
            "current": page
        },
        "error": False
    }