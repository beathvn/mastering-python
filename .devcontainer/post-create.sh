pip install poetry
poetry config virtualenvs.in-project true
poetry install
source $(poetry env info --path)/bin/activate # this makes sure we are inside the virtualenv
pre-commit install
