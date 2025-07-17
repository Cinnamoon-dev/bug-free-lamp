FROM python:3.13-slim AS build

WORKDIR /build

RUN echo "#!/bin/bash\n/.venv/bin/python3 -m src.infra.database.populate\n/.venv/bin/python3 main.py" > /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

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
COPY --from=build /docker-entrypoint.sh /

COPY . .

CMD [ "/docker-entrypoint.sh" ]