backend-install:
	@pip install --editable ".[dev]"

backend-test:
	pytest

backend-format:
	black .

backend-build:
	@python3 -m build

frontend-install:
	@npm install --prefix frontend

frontend-build:
	@npm run build --prefix frontend

frontend-watch:
	@npm run watch --prefix frontend

version:
	@echo "Next version of md2anki will be:"
	@python3 -m setuptools_scm
