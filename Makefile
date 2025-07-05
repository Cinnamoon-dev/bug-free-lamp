clean:
	rm -rf $(shell find . | grep cache)

run:
	python3 main.py