# Makefile for docker Compose management
.PHONY: down logs ps

# Default target (run the project)
default: up

# Start all containers in detached mode
up:
	docker compose up -d --build

# Stop and remove all containers
down:
	docker compose down --remove-orphans -v

# Build containers without starting
build: down
	docker compose build

# Force rebuild of containers
rebuild: down
	docker compose build --no-cache

# Clean docker environment (warning: aggressive)
fclean: down
	docker compose down -v --rmi all
	docker system prune -f

# View container logs (add service name as argument if needed)
logs:
	docker compose logs -f

log_ai:
	docker compose logs ai -f

# Show running containers
ps:
	docker compose ps

db_connect:
	docker exec -it postgres psql -U postgres -d accounting_database