pip install poetry
poetry config virtualenvs.in-project true
poetry install
source .venv/bin/activate
pre-commit install
