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
	pytest --cov=src --cov-fail-under=100