.PHONY: help install run test docker-up docker-down migrate clean

help:
	@echo "Banking API - команды для разработки"
	@echo ""
	@echo "install     - установить зависимости"
	@echo "run         - запустить сервер разработки"
	@echo "test        - запустить тесты API"
	@echo "docker-up   - запустить с помощью Docker Compose"
	@echo "docker-down - остановить Docker контейнеры"
	@echo "migrate     - запустить миграции"
	@echo "clean       - очистить временные файлы"

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	python run.py test

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
