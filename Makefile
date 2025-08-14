clean:
	rm -rf $(shell find . | grep cache)

populate:
	uv run python3 -m src.infra.database.populate

test:
	docker compose -f compose.test.yaml down -t 1
	docker compose -f compose.test.yaml up --build --abort-on-container-exit
	docker compose -f compose.test.yaml down -t 1

run:
	uv run python3 main.py