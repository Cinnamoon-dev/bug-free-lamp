import math
from typing import Any

from src.infra.database.database import PgDatabase
from src.infra.database.serializers import lines_to_dict


def paginate(
    query: str,
    page: int,
    rows_per_page: int,
    sort: str | None
) -> dict[str, Any]:
    """
    Paginates the results of an SQL query.

    Args:
        query (str): Base SQL query, without semicolon (;).
        page (int): Current page number (starting from 1).
        rows_per_page (int): Number of items per page.
        sort (str | None): Column and order for sorting, in the format "column,order".

    Returns:
        output (dict[str, Any]): Dictionary containing paginated items, pagination information, and error status.

    Raises:
        Exception: If an error occurs during query execution.
    """

    if page < 1:
        page = 1
    
    if rows_per_page < 1:
        rows_per_page = 10
    
    prev_page = page - 1
    if prev_page < 1:
        prev_page = None

    next_page = page + 1
    offset = (page - 1) * rows_per_page
    count_query = query

    if sort is not None:
        sort_column, sort_order = sort.split(",")
        query = query + f" ORDER BY {sort_column} {sort_order.upper()}"

    query = query + " LIMIT %s OFFSET %s"
    data = []

    try:
        with PgDatabase() as db:
            db.cursor.execute(f"SELECT COUNT(*) FROM ({count_query}) AS subquery")
            raw_count = db.cursor.fetchone()

            if raw_count is None:
                return {"error": True, "message": "Não foi possível fazer a query"}
            
            itens_count = raw_count[0]

            db.cursor.execute(query, (rows_per_page, offset))

            if db.cursor.description is None:
                return {"error": True, "message": "Não foi possível retonar a descrição das colunas"}

            columns = [desc[0] for desc in db.cursor.description]
            lines = db.cursor.fetchall()
            data = lines_to_dict(lines, columns)
    except Exception:
        return {"error": True, "message": "Database error"}

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