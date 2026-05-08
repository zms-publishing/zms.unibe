# zms.unibe 2026+ / Development Environment

### Python-based extensions to integrate ZMS with unibe.ch and unibe.app

This document describes the Docker-based development environment for the [ZMS](https://github.com/zms-publishing/ZMS) content management system, including the [zms.unibe](https://github.com/zms-publishing/zms.unibe) extension package.

This project provides two specialized `Dockerfiles` to support both the legacy [Zope](https://github.com/zopefoundation/Zope) stack and the modern [FastAPI](https://fastapi.tiangolo.com) stack. The `conf/` directory contains essential configuration for the Zope application server.

The [`compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml) file orchestrates a [multi-container environment](https://docs.docker.com/compose/intro/compose-application-model/) for local development. The services use [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) reflecting the changes to local code/configs in the containers instantly and restart the servers automatically.

<img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/pycharm2026.png" width="100%" />

## Repository

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

## Features

- see [`README.md`](https://github.com/zms-publishing/zms.unibe/blob/main/README.md)

## Usage

> [!NOTE]
> The preconfigured virtual environments with all dependencies installed in the containers can be customized in [`Dockerfile.zms`](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.zms) and [`Dockerfile.fastapi`](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.fastapi).

> [!TIP]
> The revisions to be used as containers can be customized to your needs by setting the variables `ZOPE_VERSION`, `ZMS_CORE_BRANCH_OR_COMMIT`, `ZMS_UNIBE_BRANCH_OR_COMMIT`, `ZMS_UNIBE_EXTRAS`, and `SETUPTOOLS_VERSION` in the `Dockerfiles` as well as the startup commands.

To start the `unibe-cms-dev` development environment:

```bash
# Clone the repository and run the containers
$ git clone https://github.com/zms-publishing/zms.unibe.git
$ docker compose up --watch

# force rebuild of the containers
$ docker compose build --no-cache
```

These directories are synchronized into the containers - see [`develop.watch` in `compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml#L18):
- Code Sync for `zms.unibe` library
  - Changes in `src/` to `/app/zope/src/zms-unibe/src`
- Config Sync for Zope application server:
  - Changes in `conf/` to `/app/zope/etc`
- Editable Dependencies for Zope/ZMS:
  - Changes in `dev/zope` and/or `dev/products-zms` if checked out

### Checkout and install the backend Python Packages on localhost

> [!CAUTION]
> The following commands demonstrate how to set up a new virtual environment on the local machine with the [latest revisions of the dependencies](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-upgrade-strategy) - these may be work-in-progress and unstable.

```bash
# Create a local virtual environment
$ cd zms.unibe
$ virtualenv .venv

# Install latest revisions of the dependencies in editable mode
$ ./.venv/bin/pip install --upgrade --upgrade-strategy=eager \
    --src ./dev -e "Zope @ git+https://github.com/zopefoundation/Zope.git@master" \
    --src ./dev -e "Products.zms @ git+https://github.com/zms-publishing/ZMS.git@main" \
    -e ../"zms.unibe[fastapi,msgraphapi,pydevd-pycharm]" \
    -c "https://raw.githubusercontent.com/zopefoundation/Zope/master/constraints.txt"
```

### Checkout and link the frontend Content Models

> [!TIP]
> The following commands demonstrate how to [check out just a single subdirectory from a large Git repository](https://gist.github.com/dinhvle/d085848c09ebd7d3a4a52de9f026c0d3). This procedure is optional.

> [!IMPORTANT]  
> The repo `github.com:idasm-unibe-ch/unibe-cms.git` is a private repository – permission is required to check it out.

```bash
# Init a Git repository, add remote
# and enable the tree check feature
$ cd dev && mkdir unibe-cms-models && cd unibe-cms-models
$ git init
$ git remote add -f origin git@github.com:idasm-unibe-ch/unibe-cms.git
$ git config core.sparseCheckout true

# Create a file in the path .git/info/sparse-checkout
# with the name of the sub directory
# you only want to checkout
$ echo 'frontend/zms/models' >> .git/info/sparse-checkout

# Download with pull, not clone
$ git pull origin main
```

## Services

- **`unibe-cms-dev`**
  - **`zms`**: The ZMS backend with [zmi](https://zope.readthedocs.io/en/latest/zopebook/UsingZope.html) and [web](https://idasm-unibe-ch.github.io/unibe-web-storybook/) frontend
    - Image: `ghcr.io/idasm-unibe-ch/unibe-cms-dev-zms:local`
    - Port: `8088` (mapped to `8080` internally)
    - ZMS: [http://127.0.0.1:8088/manage](http://localhost:8088/manage)
  - **`fastapi`**: The FastAPI frontend/API layer
    - Image: `ghcr.io/idasm-unibe-ch/unibe-cms-dev-fastapi:local`
    - Port: `5055` (mapped to `8000` internally)
    - v1: [http://127.0.0.1:5055/v1/docs](http://127.0.0.1:5055/v1/docs) (content and scheduler endpoints)
    - v3: [http://127.0.0.1:5055/v3/docs](http://127.0.0.1:5055/v3/docs) (mobile app endpoints)

## Images

- [**`Dockerfile.zms`**](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.zms): Builds the ZMS content management system.
    - Base: `ghcr.io/idasm-unibe-ch/unibe-cms:python3.14.4-zope6.1`
    - Extras: Installs `zms.unibe` with `msgraphapi` support.
    - [Entrypoint](https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/): Runs the Zope WSGI server via `runwsgi` on port 8080.

- [**`Dockerfile.fastapi`**](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.fastapi): Builds the FastAPI using ZMS headless mode.
    - Base: `ghcr.io/idasm-unibe-ch/unibe-cms:python3.14.4-zope6.1`
    - Extras: Installs `zms.unibe` with `fastapi` support.
    - [Entrypoint](https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/): Runs `fastapi dev` on port 8000.

## Configuration

- **`site.zcml`**: Zope Component registration and package includes
- **`zope.conf`**: Zope Database connections, settings, policies, etc.
- **`zope.ini`**: Zope Configuration for wsgi, waitress, waitress.queue, etc.

## License

Copyright (c) 2020-2026 [University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).
