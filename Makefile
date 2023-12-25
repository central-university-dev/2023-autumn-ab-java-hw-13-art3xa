CODE_FOLDERS := src/app src/db src/config
TEST_FOLDERS := tests


all: build down up

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

start:
	uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest --cov=src --cov-fail-under=95

lint:
	poetry run ruff $(CODE_FOLDERS)

install:
	poetry install --no-root

security_checks:
	poetry run bandit -r $(CODE_FOLDERS)
	poetry run flake8 $(CODE_FOLDERS)