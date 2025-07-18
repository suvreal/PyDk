.PHONY: install dev clean clean-build clean-cache access-venv help build example test lint type-check format

install: ## Install project in editable mode
	pip install -e .

dev: ## Install project with development dependencies
	pip install -e .[dev]

build: ## Build package (sdist + wheel)
	python -m build

example: ## Run example script
	PYTHONPATH=src python examples/py_dk_custom_facade_test.py

access-venv: ## Print manual venv activation command
	@echo "Spusť ručně: source .venv/bin/activate"

clean: clean-build clean-cache ## Clean all build artifacts and caches

clean-build: ## Clean dist, build, egg-info
	rm -rf dist build *.egg-info src/*.egg-info

clean-cache: ## Remove __pycache__ folders
	find . -type d -name "__pycache__" -exec rm -r {} +

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## Run all tests with pytest
	pytest tests/sdk_tests.py

lint: ## Run ruff and black check
	ruff check src
	black --check src

format: ## Format code with black and ruff
	ruff check --fix src
	black src

type-check: ## Run mypy static type checks
	.venv/bin/mypy src