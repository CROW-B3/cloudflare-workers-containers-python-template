APP_DIR := .

install: 
	uv sync

run: 
	uv run fastapi dev --app $(APP_DIR) --reload

run-uvicorn:
	uvicorn main:app --host 0.0.0.0 --port 8080 --loop uvloop --workers 2 --http httptools

lint: 
	uv run ruff check .

format: 
	uv run ruff format .

clean: 
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache build dist *.egg-info .coverage htmlcov *.log out/
