# Mastering python

collecting useful information

- [Mastering python](#mastering-python)
  - [WSL](#wsl)
  - [MacOS docker daemon - colima](#macos-docker-daemon---colima)
  - [Dev Container](#dev-container)
    - [Troubleshooting](#troubleshooting)
  - [Poetry](#poetry)
    - [Useful commands](#useful-commands)
    - [Versions](#versions)
  - [uv](#uv)
  - [Git pre-commits](#git-pre-commits)
  - [Terraform](#terraform)
    - [Working locally with terraform](#working-locally-with-terraform)
  - [Docker](#docker)
  - [Terminal](#terminal)
  - [Markdown](#markdown)

## WSL

If you want to run dev-container on windows, you need a docker engine. Docker desktop is the easiest way, but for industries of a certain size, you cannot use it. So your best option is to install wsl and use the docker cli (which is free).
If you choose Ubuntu as your distribution that runs on top of WSL2, regularly check the size of the App ubuntu in windows, because it can grow really large (up to a point where the C: drive is completly full!). To shrink the size of the Ubuntu app follow these steps:

- cleanup in wsl itself. Follow this:
  - if using docker, check the docker section below on how to clean that.
  - `du -a FOLDERPATH | sort -n -r | head -n 5` to list the top 5 folders taking up space
  - shutdown wsl
  - open up powershell as admin and execute this command `Optimize-VHD -Path "C:\Users\<username>\AppData\Local\Packages\...\LocalState\ext4.vhdx" -Mode Full` (it can be that it fails, because it is used by another process... just wait a bit)

Useful commands

- `wsl --list --verbose`: lists the available distributions
- `wsl --shutdown`

## MacOS docker daemon - colima

Colima gives you a docker daemon (needed for dev container) on the mac. You can install it with brew. Use the following commands:

- `colima start`: starts the daemon (with default settings)
- `colima start --cpus 4 --memory 8`: starts the daemon with 4 cpus and 8gb of memory
- `colima stop`: stops the daemon

## Dev Container

Lets you run your development environment in a container. This is useful, if you want to have a consistent environment across different machines.
If you want to install something new into your dev environment (not a simple dependency, but something more on system level) there are 2 ways to do it:

- with the Dockerfile
- with the devcontainer.json using features (this is more simple and recommended for things that you just need for development and not production). see here for the [available feature](https://containers.dev/features). These can be configured and don't need to be maintained by you. It is also possible that some vs code extensions are installed with a feature.

### Troubleshooting

- If you get the error, that you cannot edit or create files, once opened in the dev container, the problem could be that you have configured the environment from where you start it to use a root user. In the dev container configuration it defines a non-root user called vscode to be used in the container. You can remove all of that (not recommended, as it is best practice to use a non-root user in the container) to load the container as root user.

## Poetry

This lets you easily manage dependencies in python.

### Useful commands

Here are some useful commands:

- **poetry add**
  - `poetry add pytest` to install pytest and add that to the pyproject.toml file.
  - `poetry add --group dev pytest` to add it to the dev dependencies
  - `poetry source add --priority=explicit privatesource https://pkgs.dev.azure.com/<ORG>/<PROJECT>/_packaging/privatly-hosted-package/pypi/simple/`. Sets up privatesource as a source for packages. See here for [docu](https://python-poetry.org/docs/repositories/). Using Azure-DevOps Artifacts in this case.
  - `poetry add privatly-hosted-package --source privatesource` to add a package from privatesource. privatesource needs to be setup prior to this.
  - `poetry add --editable ./path/to/lib` to add a package in editable mode - changed are reflected instatly.
- `poetry remove pytest` removes that dependency (and all its dependencies!)
- `poetry update pytest` updates the package to the latest version
- **poetry install**
  - `poetry install` installs all the dependencies from the [pyproject.toml](./pyproject.toml), including the ones within eventual subgroups (if they are not optional). Use the `--with` flag, to include the optional dependencies (by providing the name).
  - `poetry install --no-root` the current project is NOT installed in editable mode (which is default). This affects a single execution of poetry install. `package-mode = false` in [pyproject.toml](./pyproject.toml) is a project-wide setting that changes Poetry's behavior for all relevant commands (also the `poetry install` command)
  - `poetry install --without dev` installs without the dev group deps
- **poetry show**
  - `poetry show` gives an overall look of your dependencies in the environment.
  - `poetry show requests` shows the version of the package.
  - `poetry show --tree` to show the whole dependency tree.

### Versions

The '^' sign for a version (in [pyproject.toml](./pyproject.toml)), allows updates for minor versions, but nor for major versions. This is the default behaviour, when simply adding a package with `poetry add requests`.
To control the version that is installed you can use:

- `poetry add requests@2.12.1` to install a specific version
- `poetry add requests^2.12.1` to install the most recent minor-version following the `2.12.1` version, but it won't install `3.x.x`. This is the default behavior.
- `poetry add requests~2.12.1` to install the most recent patch-version following the `2.12.1` version, but it won't install `2.13.x`.

## uv

let's you also manage dependencies like poetry but is faster. Read the [docs](https://docs.astral.sh/uv/).

Useful commands for a single script:

- **python versions**
  - `uv python list` lists all available python versions and shows which ones are installed
  - `uv python install 3.11` installs the given version
- **run scripts**
  - `uv run script.py` runs the script with default python version
  - `uv run --python 3.11 script.py` runs the script with the given python version
  - `uv run --python 3.11 --with numpy script.py` runs the script with the given python version and the given dependency. Add more dependencies with `--with` flag.
  - `uv init --script script.py --python 3.11` adds a comment to the script, that shows which python version are needed to run the script
  - `uv add --script script.py "numpy"` adds the dependency to the script (in the comments that where been added on top of the script)
- **with python projects**
  - **uv init** (read the [docs](https://docs.astral.sh/uv/concepts/projects/init/))
    - `uv init example-app` init git repo, creates a bunch of files. If you don't pass the name, it will use the current folder name.
    - `uv init --lib numbers` inits the folder structure for a library called numbers
    - `uv init --no-workspace` useful when you need to init a uv project inside another uv project. If you just do `uv init` it will create a workspace and add the current project to the workspace (no seperate .venv for inner project...)
  - **uv add**
    - `uv add numpy` adds the dependency to the project (creates also a .venv folder in the project for the first extra dependency added)
    - `uv add numpy --editable path/to/library` adds the dependency in editable mode
    - to add packages from a private source follow this [documentation](https://docs.astral.sh/uv/guides/integration/alternative-indexes/). In a nutshell: you need to set the environmental variables (that depend on the index name: `UV_INDEX_PRIVATE_REGISTRY_USERNAME`, `UV_INDEX_PRIVATE_REGISTRY_PASSWORD` if index name is `private-registry`) and can then install the package with `uv add <package> --index <index-name>=<index-url>`. No need to edit the `.toml` file manually.
  - `uv remove numpy` removes the dependency from the project
  - `uv run main.py` equivalent to the script part
  - `uv sync` syncs the dependencies with the virtual environment - this automatically runs before `uv run` command
  - `uv lock` creates lock files

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

- **free up space**
  - `docker system df`: lets you see how much space is used by images, containers and volumes
  - `docker system prune -a`: removes all images, containers and volumes that are not used
  - `docker images`: shows all images
  - `docker rmi IMAGE_ID`: removes the image with the given id
  - `docker rm CONTAINER_ID`: removes the container with the given id
  - `docker image prune`: removes all dangling images
  - `docker builder prune`: removes the build cache of all images
    - `docker builder prune --all`: removes all the build cache, even the ones that are still used by images
    - `docker builder prune --filter until=24h`: removes build cache older than 24 hours
  - **docker volumes** this is also used by docker-in-docker
    - `docker volume ls`: lists the volumes
    - `docker volume rm VOLUME_NAME`: removes the volume
- **azure container registry:** how to interact with ACR.
  - **login** on CLI ([read the docs](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli)):
    - `az acr login --name <registry-name>`
    - `docker login -u <tokenname> -p <password> <registry-name>.azurecr.io` login using token
  - **push** an image:
    - first tag the image: `docker tag <local-imagename>:<TAG> <registry-name>.azurecr.io/<repo-name>:<TAG>`
    - push the image: `docker push <registry-name>.azurecr.io/<repo-name>:<TAG>`
  - **pull** an image:
    - `docker pull <registry-name>.azurecr.io/<repo-name>:<TAG>`

## Terminal

Using oh-my-zsh to use the different plugins. These are some useful plugins. You need to clone the repo with the provided command and then add it to the `.zshrc` file. To do this use `nano ~/.zshrc`.

- **zsh-autosuggestions**: suggests commands based on your history. cmd: `git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`. This plugin takes suggestions also from the `~/.zsh_history` file.
- **zsh-syntax-highlighting**: highlights the command you are typing. cmd: `git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`

## Markdown

> [!NOTE]
> for these to work you need the `yzhang.markdown-all-in-one` extension installed
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
