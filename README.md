# SQL Boilerplate
A simple FastAPI application with raw SQL queries using `psycopg2`. The database connection is made using an `Database` abstract class, so it is possible to change drivers without much trouble.

### Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv)