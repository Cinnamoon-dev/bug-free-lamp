from typing import Any

        
def line_to_dict(line: tuple[Any], columns: list[str]) -> dict[str, Any]:
    """
    Converts a single database row (tuple) into a dictionary mapping column names to values.

    Args:
        line (tuple[Any]): A tuple representing a row returned from a SELECT query.
        columns (list[str]): List of column names, in the same order as in the SELECT statement.

    Returns:
        output (dict[str, Any]): Dictionary where keys are column names and values are the corresponding row values.

    Example:
        ```python
        columns = ["id", "email", "user_type"]
        line = (1, "user@email.com", "admin")
        result = {"id": 1, "email": "user@email.com", "user_type": "admin"}
        ```
    """
    line_dict = {}
    for index, column in enumerate(columns):
        line_dict[column] = line[index]

    return line_dict

def lines_to_dict(lines: list[tuple[Any]], columns: list[str]) -> list[dict[str, Any]]:
    """
    Converts a list of database rows (tuples) into a list of dictionaries mapping column names to values.

    Args:
        lines (list[tuple[Any]]): List of tuples, each representing a row from a SELECT query.
        columns (list[str]): List of column names, in the same order as in the SELECT statement.

    Returns:
        output (list[dict[str, Any]]): List of dictionaries, each mapping column names to row values.

    Example:
        ```python
        columns = ["id", "email"]
        lines = [(1, "a@email.com"), (2, "b@email.com")]
        result = [{"id": 1, "email": "a@email.com"}, {"id": 2, "email": "b@email.com"}]
        ```
    """
    serialized_lines = []
    for line in lines:
        serialized_lines.append(line_to_dict(line, columns))

    return serialized_lines