dev_up:
	docker compose up -d

dev_down:
	docker compose down --remove-orphans && docker volume prune -f && docker image rm fast_api_build

include .env.dev
export

run_server:
	uvicorn src.application.api.main:app --reload

dev_migration:
	alembic revision --autogenerate -m "Initial tables"

dev_upgrade:
	alembic upgrade head
