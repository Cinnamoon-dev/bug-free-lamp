clean:
	rm -rf $(shell find . | grep cache)

test:
	docker compose -f compose.test.yaml up --build --abort-on-container-exit
	docker compose -f compose.test.yaml down -t 1

run:
	python3 main.py