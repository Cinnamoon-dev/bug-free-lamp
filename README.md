# SQL Boilerplate
A simple FastAPI application with raw SQL queries using context managers and injecting the SQL driver module.

The database connection is made using an `Database` abstract context manager, so it is possible to change drivers without much trouble.

### Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv)

### Running Project
Default values for the `.env` files are already set in the dev compose. 
```bash
docker compose -f compose.dev.yaml up --build -d
```

### Swagger
Access swagger at `localhost:8000/docs`.

    Mocked user
    email: admin@email.com
    password: 1234

### Project Features
- Authentication with JWT and OAuth2
- Permission management with rules table
- Testing pipeline with Github Actions + Docker
- Unit tests with Pytest
- Pagination module
- Schema creation with Pydantic