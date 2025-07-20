import math
from typing import Any
from fastapi.datastructures import QueryParams

from src.infra.database.database import PgDatabase
from src.infra.database.serializers import lines_to_dict


def paginate(
    table_name: str, 
    columns: list[str], 
    query_params: QueryParams
) -> dict[str, Any]:
    page = int(query_params.get("page", 1))
    rows_per_page = int(query_params.get("rows_per_page", 10))
    # TODO
    # query_params.get("sort", "id|ASC")

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

    with PgDatabase() as db:
        db.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        raw_count = db.cursor.fetchone()

        if raw_count is None:
            return {"error": True, "message": "Não foi possível fazer a query"}
        
        itens_count = raw_count[0]

        db.cursor.execute(f"SELECT {columns_string} FROM {table_name} LIMIT (%s) OFFSET (%s)", (rows_per_page, offset))
        lines = db.cursor.fetchall()

        data = lines_to_dict(lines, columns)

    pages_count = math.ceil(itens_count / rows_per_page)

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