POETRY_EXEC=poetry
PYTHON_EXEC = $(POETRY_EXEC) run python
TOML_FILES=poetry.lock pyproject.toml
MYPY_OPTS = --ignore-missing-imports
LINTER_DIRS=app
FORMAT_DIRS=app
AUTOFLAKE_OPTS = -i -r --verbose --ignore-init-module-imports --remove-all-unused-imports --expand-star-imports --exclude=migration

lint: autoflake flake8 pylint
com: autoflake flake8 pylint pytest

autoflake:
	$(PYTHON_EXEC) -m autoflake $(AUTOFLAKE_OPTS) $(FORMAT_DIRS)

mypy:
	$(POETRY_EXEC) run mypy --show-error-codes --python-version=3.12 $(LINTER_DIRS)

flake8:
	$(POETRY_EXEC) run flake8 --jobs 4 --statistics --show-source $(LINTER_DIRS) --exclude=migration

pylint:
	$(POETRY_EXEC) run pylint --jobs 4 --rcfile=setup.cfg --extension-pkg-whitelist='pydantic' --ignore=migration $(LINTER_DIRS) 

toml-sort:
	$(POETRY_EXEC) run toml-sort $(TOML_FILES) -i -a

app:
	python main.py

pytest:
	pytest -vv -s app/tests

pytest-cov:
	pytest --cov=app -vv app/tests

b:
	docker-compose up --build

u:
	uvicorn app.main:app

migrate:
	@echo "Введите описание миграции:"
	@read -p "> " message; \
	alembic revision --autogenerate -m "$$message"

upgrade:
	alembic upgrade head


.PHONY: all-linters mypy flake8 pylint toml-sort autoflake app pytest pytest-cov
