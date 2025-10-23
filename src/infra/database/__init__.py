from src.infra.database.database import PgDatabase


def retrieve_table_columns(table_name: str) -> list[str]:
    """
    Retrieves the list of column names for a given table from the PostgreSQL database.

    Args:
        table_name (str): The name of the table to fetch column names from.

    Returns:
        output (list[str]): A list containing the names of the columns in the specified table.

    Example:
        ```python
        columns = get_table_columns("users")
        # columns -> ["id", "email", "created_at"]
        ```
    """
    with PgDatabase() as db:
        db.cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
            (table_name,),
        )
        columns = [row[0] for row in db.cursor.fetchall()]

    return columns
