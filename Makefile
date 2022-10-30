.PHONY: lint
lint:
	black app
	isort app

.PHONY: connect
connect:
	docker-compose exec backend bash
.DEFAULT_GOAL :=
