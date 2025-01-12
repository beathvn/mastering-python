# Mastering python

collecting useful information

## Poetry
This lets you easily manage dependencies in python. This '^' sign for a version (in [pyproject.toml](./pyproject.toml)), allows updates for minor versions, but nor for major versions. This is the default setting.

Here are some useful commands:
* `poetry add pytest` to install pytest and add that to the pyproject.toml file
* `poetry remove pytest` removes that dependency (and all its dependencies!)
* `poetry add --group dev pytest` to add it to the dev dependencies
* `poetry install` installs all the dependencies from the [pyproject.toml](./pyproject.toml), including the ones within eventual subgroups
* `poetry install --no-root` the current project is NOT installed in editable mode (which is default). This affects a single execution of poetry install. `package-mode = false` in [pyproject.toml](./pyproject.toml) is a project-wide setting that changes Poetry's behavior for all relevant commands (also the `poetry install` command)
* `poetry install --without dev` installs without the dev group deps
* `poetry install --compile` useful for dockerfiles: creates python bytecode from the sources. Speeds up start time. This is something that also happens when you first run source code. Python bytecode is portable across operating systems, but not across versions of Python. Most importantly: bytecode files are marked with the version they're supposed to run with. If it doesn't match what the interpreter is expecting, it will just re-compile the bytecode.
