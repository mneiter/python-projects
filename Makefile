.PHONY: help up down build lint format test

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make up        - Start all Docker containers using docker-compose"
	@echo "  make down      - Stop all running Docker containers"
	@echo "  make build     - Build the Docker image for the Python app"
	@echo "  make lint      - Run code linters and type checks"
	@echo "  make format    - Auto-format code using black and isort"
	@echo "  make test      - Run all unit tests with pytest"

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
