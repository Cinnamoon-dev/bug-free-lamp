from typing import Any

        
def line_to_dict(line: tuple[Any], columns: list[str]) -> dict[str, Any]:
    """
        Transforms a database `SELECT` tuple in a dictionary.

        `@columns` elements should be in the same order as the `SELECT` query.\n
        Example: `columns = ["id", "email", "user_type"]` -> `SELECT id, email, user_type ...`
    """
    line_dict = {}
    for index, column in enumerate(columns):
        line_dict[column] = line[index]

    return line_dict

def lines_to_dict(lines: list[tuple[Any]], columns: list[str]) -> list[dict[str, Any]]:
    """
        Transforms database `SELECT` tuples in a list of dictionaries.

        `@columns` elements should be in the same order as the `SELECT` query.\n
        Example: `columns = ["id", "email", "user_type"]` -> `SELECT id, email, user_type ...`
    """
    serialized_lines = []
    for line in lines:
        serialized_lines.append(line_to_dict(line, columns))

    return serialized_lines