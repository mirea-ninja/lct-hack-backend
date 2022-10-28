.PHONY: lint
lint:
	black app
	isort app

.DEFAULT_GOAL :=
