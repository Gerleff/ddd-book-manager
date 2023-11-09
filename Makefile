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

test:
	# ******* Pytest *******
	poetry run pytest tests
