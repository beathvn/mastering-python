# Mastering python

collecting useful information

## Dev Container
Lets you run your development environment in a container. This is useful, if you want to have a consistent environment across different machines.
If you want to install something new into your dev environment (not a simple dependency, but something more on system level) there are 2 ways to do it:
* with the Dockerfile
* with the devcontainer.json using features (this is more simple and recommended for things that you just need for development and not production). see here for the [available feature](https://containers.dev/features). These can be configured and don't need to be maintained by you. It is also possible that some vs code extensions are installed with a feature.


### Troubleshooting
* If you get the error, that you cannot edit or create files, once opened in the dev container, the problem could be that you have configured the environment from where you start it to use a root user. In the dev container configuration it defines a non-root user called vscode to be used in the container. You can remove all of that (not recommended, as it is best practice to use a non-root user in the container) to load the container as root user.

## Poetry
This lets you easily manage dependencies in python.

### Useful commands
Here are some useful commands:
* `poetry add pytest` to install pytest and add that to the pyproject.toml file.
* `poetry remove pytest` removes that dependency (and all its dependencies!)
* `poetry add --group dev pytest` to add it to the dev dependencies
* `poetry install` installs all the dependencies from the [pyproject.toml](./pyproject.toml), including the ones within eventual subgroups (if they are not optional). Use the `--with` flag, to include the optional dependencies (by providing the name).
* `poetry install --no-root` the current project is NOT installed in editable mode (which is default). This affects a single execution of poetry install. `package-mode = false` in [pyproject.toml](./pyproject.toml) is a project-wide setting that changes Poetry's behavior for all relevant commands (also the `poetry install` command)
* `poetry install --without dev` installs without the dev group deps
* `poetry install --compile` useful for dockerfiles: creates python bytecode from the sources. Speeds up start time. This is something that also happens when you first run source code. Python bytecode is portable across operating systems, but not across versions of Python. Most importantly: bytecode files are marked with the version they're supposed to run with. If it doesn't match what the interpreter is expecting, it will just re-compile the bytecode.
* `poetry show requests` shows the version of the package. You can also use `poetry show --tree` to show the whole dependency tree. For a more simple look at your environment, you can simply use `poetry show`

### Versions
The '^' sign for a version (in [pyproject.toml](./pyproject.toml)), allows updates for minor versions, but nor for major versions. This is the default behaviour, when simply adding a package with `poetry add requests`.
To control the version that is installed you can use:
* `poetry add requests@2.12.1` to install a specific version
* `poetry add requests^2.12.1` to install the most recent minor-version following the `2.12.1` version, but it won't install `3.x.x`. This is the default behavior.
* `poetry add requests~2.12.1` to install the most recent patch-version following the `2.12.1` version, but it won't install `2.13.x`.

## Git pre-commits
Define some hooks, that should run before you commit anything. In this file [.pre-commit-config.yaml](./.pre-commit-config.yaml), you define the pre-commit hooks that should run, and with `pre-commit install` you install them.

To test the pre-commit hooks, you can use `pre-commit run --all-files`

For local scripts, you need to make sure, they are executable (otherwise you will get an error telling you they are not executable). You can do this with `chmod +x <scriptname>`

## Terraform
### Working locally with terraform
This guide (got from these [docs](https://developer.hashicorp.com/terraform/language/backend/azurerm)) will show you, how to setup the terraform backend to work with terraform statefiles in an Azure Storage Account.
1. `az login` with the user you want to use for terraform. Use `az account show` to see the current account.
2. Make sure your user has the following permissions on the storage account: `Storage Blob Data Owner` or `Container Blob Data Owner`
3. set the following environment variables (you could simply define them in a `.env` file and load that file with `set -a` and `source .env`):
    ```shell
    ARM_USE_AZUREAD=true
    ```
4. Run the following `$ terraform init \
    -backend-config="resource_group_name=YOUR_RESOURCE_GROUP_NAME" \
    -backend-config="storage_account_name=YOUR_STORAGE_ACCOUNT_NAME" \
    -backend-config="container_name=YOUR_CONTAINER_NAME" \
    -backend-config="key=YOUR_BLOB_NAME.tfstate"`

## Docker
If you build a lot of docker images you need to make sure that you clean them also. Here are some useful commands
* `docker system df`: lets you see how much space is used by images, containers and volumes
* `docker images`: shows all images
* `docker rmi IMAGE_ID`: removes the image with the given id
* `docker image prune`: removes all dangling images
* `docker builder prune`: removes the build cache of all images
* `docker builder prune --all`: removes all the build cache, even the ones that are still used by images
* `docker builder prune --filter until=24h`: removes build cache older than 24 hours

## Terminal
Using oh-my-zsh to use the different plugins. These are some useful plugins. You need to clone the repo with the provided command and then add it to the `.zshrc` file. To do this use `vi ~/.zshrc`. Hit `i` to enter insert mode. Add the plugin to the plugins array (space separated list). Hit `esc` to leave insert mode. Type `:wq` to save and quit. After that restart the terminal.
* **zsh-autosuggestions**: suggests commands based on your history. cmd: `git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`. This plugin takes suggestions also from the `~/.zsh_history` file.
* **zsh-syntax-highlighting**: highlights the command you are typing. cmd: `git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`