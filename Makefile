.PHONY: help up down build lint format test clean logs restart shell

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make up        - Start all Docker containers using docker-compose"
	@echo "  make down      - Stop all running Docker containers"
	@echo "  make build     - Build the Docker image for the Python app"
	@echo "  make lint      - Run code linters and type checks"
	@echo "  make format    - Auto-format code using black and isort"
	@echo "  make test      - Run all unit tests with pytest"
	@echo "  make clean     - Remove all __pycache__ and *.pyc files"
	@echo "  make logs      - Show logs from the main app container"
	@echo "  make restart   - Restart the main app container"
	@echo "  make shell     - Open shell inside the main app container"

# Start all services using docker-compose
up:
	docker-compose up -d

# Stop and remove all running services
down:
	docker-compose down

# Build the Docker image defined in docker-compose
build:
	docker-compose build

# Run linting and static analysis tools
lint:
	./run-lint.sh

# Format the codebase using black and isort
format:
	black .
	isort .

# Run unit tests using pytest
test:
	pytest tests/

# Remove Python cache files and artifacts
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete

# Show logs from the Python app container
logs:
	docker logs -f python-app

# Restart the main app container
restart:
	docker-compose restart python-app

# Open interactive shell in the app container
shell:
	docker exec -it python-app bash
