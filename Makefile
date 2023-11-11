formatters:
	# ******* Black *******
	black src --line-length=120
	# ******* iSort *******
	isort src

linters:
	# ******* Flake8 *******
	flake8 src

deploy:
	# ******* Docker *******
	docker-compose up

makemigration:
	# ******* Pytest *******
	poetry run alembic upgrade head

test:
	# ******* Pytest *******
	poetry run pytest tests
