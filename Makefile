.PHONY: format
format:
	isort --force-single-line-imports app
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
	black app
	isort app

.PHONY: connect
connect:
	docker-compose exec backend bash

.PHONY: logs
logs:
	docker logs --follow lct-hack-backend-backend-1


.PHONY: clear
clear:
	docker-compose down
	docker volume prune || true
	docker-compose up -d --build

.DEFAULT_GOAL :=

