FROM python:3.13-slim AS build

WORKDIR /build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml .python-version /build/

RUN uv sync --no-cache

FROM python:3.13-slim AS test

WORKDIR /app

COPY --from=build /build/.venv /.venv

COPY . .

CMD ["/.venv/bin/python3", "-m", "pytest"]

FROM python:3.13-slim AS runtime

WORKDIR /app

COPY --from=build /build/.venv /.venv

COPY . .

CMD ["/.venv/bin/python3", "main.py"]