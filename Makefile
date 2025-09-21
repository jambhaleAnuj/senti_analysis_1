PY=python

.PHONY: install dev lint format test run docker-build docker-run

install:
	$(PY) -m pip install -r requirements.txt

dev: install
	$(PY) -m pip install -r requirements-dev.txt

lint:
	ruff check .

format:
	black .
	ruff check --fix .

test:
	pytest -q

run:
	$(PY) app.py

docker-build:
	docker build -t movie-sentiment:latest .

docker-run:
	docker run --rm -p 5000:5000 --env-file .env movie-sentiment:latest
