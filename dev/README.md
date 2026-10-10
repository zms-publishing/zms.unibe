# zms.unibe / Development Environment

### Integrate ZMS with unibe.ch and unibe.app

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

This `zms.unibe` comprehensive Python library extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality.

It includes several modules specific for the [University of Bern (UniBE)](https://unibe.ch) in Switzerland – as well as a set of [helper functions](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md) that can be useful in `Page Templates` or `Python Scripts` in any ZMS/Zope-based CMS.

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
- [Environments](#environments)
  - [Start the container environment](#start-the-container-environment)
  - [Checkout and install on localhost](#checkout-and-install-on-localhost)
  - [Setup and run on localhost](#setup-and-run-on-localhost)
  - [Checkout and link the content models](#checkout-and-link-the-content-models)
- [Services](#services)
- [Images](#images)
- [Configs](#configs)
- [License](#license)

## Overview

This package includes modules for agenda management, announcements, contacts, data tables, forms and surveys, layouts, mobile app support, and more.

It features a fully decoupled, [headless RESTful API](https://idasm-unibe-ch.github.io/unibe-web-mobile/CMSAPI/) for accessing the content objects stored in [ZODB](https://zodb.org), using the ~~web application (micro)framework Flask~~ [FastAPI](https://fastapi.tiangolo.com) framework, which is served by [Uvicorn](https://www.uvicorn.dev).

In addition, it relies on ~~Flasgger to generate the documentation~~ [SQLModel](https://sqlmodel.tiangolo.com) for implementing an object-relational mapping.

Furthermore, it can connect to [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/overview) as the gateway to data and intelligence in Microsoft cloud services like [M365](https://learn.microsoft.com/en-us/graph/overview) or [Entra](https://learn.microsoft.com/en-us/graph/identity-network-access-overview) if the `[msgraphapi]` extra has been applied on installation.

This solution architecture, based on modern [Python](https://www.python.org) frameworks, unlocks a more lightweight development mode alongside the historically grown Zope stack.

<img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/zms6.png" width="33%" /> <img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/fastapi1.png" width="33%" /> <img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/fastapi3.png" width="33%" />

## Usage

This project provides two specialized `Dockerfiles` to support both the legacy [Zope](https://github.com/zopefoundation/Zope) stack and the modern [FastAPI](https://fastapi.tiangolo.com) stack. The `conf/` directory contains essential configuration for the Zope application server.

The [`compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml) file orchestrates a [multi-container environment](https://docs.docker.com/compose/intro/compose-application-model/) for local development. The services use [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) reflecting the changes to local code/configs in the containers instantly and restart the servers automatically.

<details>
<summary>Project Structure</summary>

```
zms.unibe
├── LICENSE
├── README.md
├── pyproject.toml
├── constraints.txt
├── Dockerfile.fastapi
├── Dockerfile.zms
├── alembic.ini
├── compose.yaml
├── compose.dev.yaml
├── compose.empty.yaml
├── versions.env
├── alembic
│   ├── versions
│   ├── env.py
│   └── README.md
├── app
│   └── main.py [FastAPI main app]
├── cron
│   ├── [scheduled jobs]
│   └── ...
├── conf
│   ├── zodb-relstorage.conf
│   ├── zodb-zeo.conf
│   ├── zope.conf
│   ├── zope.ini
│   └── ...
├── dev
│   ├── [local checkouts in editable mode]
│   ├── README.md
│   └── ...
└── src
    └── zms
        └── unibe
            ├── agenda
            │   ├── schemas
            │   └── sqlmodels
            ├── ...
            ├── fastapi
            │   ├── mobileapp
            │   ├── zmscontent
            │   └── main.py [FastAPI sub apps]
            ├── ...
            ├── patches
            │   ├── monkey
            │   ├── security
            │   └── configure.zcml
            └── utils
                ├── zms2sql
                ├── zope
                ├── db.py
                ├── dependencies.py
                ├── enums.py
                ├── helpers.py
                └── subscribers.py
```

</details>

<details>
<summary>Feature Overview</summary>
<br />

| <nobr>Integrate with other services</nobr>                                                                                                                 | <nobr>Extend existing funtionality</nobr> | <nobr>Handle content objects</nobr>                                                          |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------|:---------------------------------------------------------------------------------------------|
| [DataTables.net](https://datatables.net) samples                                                                                                           | Database utilities                        | [SQLModels](https://sqlmodel.tiangolo.com/) (ZMSBase, ZMSSite, ZMSFolder, ZMSDocument, etc.) |
| [BORIS](https://boris.unibe.ch) connector                                                                                                                  | Helper functions and enums                | Graphic and File handling, Content panes and tabs                                            |
| Outlook connector for [calendar integration via MS Graph API](https://learn.microsoft.com/en-us/graph/api/resources/calendar-overview?view=graph-rest-1.0) | Context management                        | Tables and Text areas, Code blocks                                                           |
| Agenda bridge for flexible data aggregation                                                                                                                | Scheduler registry                        | Alert boxes, Info boxes, News boxes                                                          |
| Event schemas and SQL models                                                                                                                               | `zms2sql` command-line tool               | Hero components, Teaser containers and elements                                              |
| Library and news integration                                                                                                                               | `MemCached` error handling                | Media releases, Article management and Factsheet layouts                                     |
| IT status messages                                                                                                                                         | <nobr>`ExternalMethod` auto-reload</nobr> | Contact boxes and sections, Persons and Team sections                                        |
| Form management based on [JSON Editor](https://github.com/json-editor/json-editor) and [SurveyJS](https://surveyjs.io)                                     | Security assertions                       | Two-column layouts                                                                           |

</details>

<details>
<summary>Dependencies</summary>
<br />

The package requires [Python 3.11+](https://www.python.org/downloads/) and depends on

- **Application Server**: `Zope`, `Products.PluggableAuthService`, `Products.mcdutils`
- **Database**: `SQLAlchemy`, `SQLModel`, `relstorage`, `psycopg2`, migration with `[alembic]` extra
- **Web/API**: `FastAPI`, `starlette`, `pydantic`, `requests`, `uvicorn` with `[fastapi]` extra
- **Utilities**: `typer`, `rich`, `python-dotenv`, `devtools`, debugger with `[pydevd-pycharm]` extra
- **Office Integration**: `XlsxWriter`, `azure-identity`, `msgraph-sdk` with `[msgraphapi]` extra
- **Data Processing**: `pandas`, `beautifulsoup4`, `lxml`, `MarkItDown`, `rq` with `rq-dashboard-fast`

See [`pyproject.toml`](https://github.com/zms-publishing/zms.unibe/blob/main/pyproject.toml) for the complete list and references of dependencies and [`constraints.txt`](https://github.com/zms-publishing/zms.unibe/blob/main/constraints.txt) for their pinned versions.

</details>

<details>
<summary>Utilities</summary>
<br />

The package provides the `zms2sql` command-line tool for object-relational mappings to mirror selected data from the [ZODB](https://zodb.org) to [PostgreSQL](https://www.postgresql.org), for example:

```bash
$ ./.venv/bin/zms2sql --help
```

To apply the [monkey patches](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/patches/monkey) for customizing other installed packages as well as the [security assertions](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/patches/security) for using the helper utilities in [RestrictedPython](https://github.com/zopefoundation/RestrictedPython) code (py, zpt, dtml), the following package include must be added to the `./.venv/etc/site.zcml` file:

```xml
<configure xmlns:zcml="http://namespaces.zope.org/zcml">
  <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
</configure>
```

This allows editing via the web using [ZMI](https://zope.readthedocs.io/en/latest/zopebook/UsingZope.html) or synchronize code changes via the [ZMSRepositoryManager](https://github.com/zms-publishing/ZMS/tree/main/Products/zms/zpt/ZMSRepositoryManager/readme.md).

To enable support for [Remote Debugging with PyCharm](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html) you can include the `[pydevd-pycharm]` extra on installation.

See [`alembic/README.md`](https://github.com/zms-publishing/zms.unibe/blob/main/alembic/README.md) for SQL Database schema migrations.

</details>

## Environments

### Start the container environment

> [!NOTE]
> The revisions to be used as containers can be customized to your needs by setting the variables `BASE_IMAGE`, `ZOPE_VERSION`, `ZMS_CORE_BRANCH_OR_COMMIT`, `ZMS_UNIBE_BRANCH_OR_COMMIT`, and `SETUPTOOLS_VERSION` in the [`versions.env`](https://github.com/zms-publishing/zms.unibe/blob/main/versions.env) file and their defaults in [`build.args` in `compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml#L18). The container installation procedures can be customized in [`Dockerfile.zms`](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.zms) and [`Dockerfile.fastapi`](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.fastapi).

> [!IMPORTANT]
> The base image `ghcr.io/idasm-unibe-ch/unibe-cms` is required to build on top of – permission is required to check it out. In addition, it is expected that the `zeo`, `memcached`, and `psql` containers from the `unibe-cms` stack are running to provide the data storages.

```bash
# Get the project
$ git clone https://github.com/zms-publishing/zms.unibe.git

# Set the build environment from versions.env
# and check the resolved variables
# -> run this every time you change versions.env
$ export $(xargs < versions.env) && docker compose config

# Force rebuild of the containers
$ docker compose build --no-cache

# Run the containers watching for file changes in defined directories
$ docker compose up --watch
```

These directories are synchronized into the containers - see `develop.watch` in [`compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml#L28) and [`compose.dev.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.dev.yaml)
- Code Sync for `zms.unibe` library
  - Changes in `src/` to `/app/zope/src/zms-unibe/src`
- Config Sync for Zope application server:
  - Changes in `conf/` to `/app/zope/etc`
- Lifecycle Manager for the FastAPI main app:
  - Changes in `app/` to `/app/zope/src/zms-unibe/app`
- Editable Dependencies for Zope/ZMS:
  - Changes in `dev/zope` and/or `dev/products-zms` if checked out and set `COMPOSE_INCLUDE=dev` in `versions.env`

### Checkout and install on localhost

> [!CAUTION]
> The following commands demonstrate how to set up a new virtual environment on the local machine with the [latest revisions of the dependencies](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-U) omitting the pinned versions in [`zms.unibe/constraints.txt`](https://github.com/zms-publishing/zms.unibe/blob/main/constraints.txt) – these may be work-in-progress and unstable.

```bash
# Create a local virtual environment
$ cd zms.unibe
$ virtualenv .venv

# Install Zope/ZMS as editable dependencies
# using the revisions defined in versions.env file
# and checked out as git repos in the ./dev directory
# -> will be linked into the containers by COMPOSE_INCLUDE=dev in versions.env
$ export $(xargs < versions.env) && ./.venv/bin/pip install --upgrade pip wheel setuptools==$SETUPTOOLS_VERSION
$ export $(xargs < versions.env) && ./.venv/bin/pip install --upgrade --upgrade-strategy eager \
    --src ./dev -e "Zope @ git+https://github.com/zopefoundation/Zope.git@$ZOPE_VERSION" \
    --src ./dev -e "ZMS @ git+https://github.com/zms-publishing/ZMS.git@$ZMS_CORE_BRANCH_OR_COMMIT" \
    -e ../"zms.unibe[zope,fastapi,msgraphapi,pydevd-pycharm,alembic]" \
    -c "https://raw.githubusercontent.com/zopefoundation/Zope/$ZOPE_VERSION/constraints.txt"
```

### Setup and run on localhost

> [!TIP]
> The following commands provide a plain Zope installation with default settings and an initial database in the local virtual environment. It can be used in parallel to the container environment.

```bash
# Create default directories for Zope instance home
# -> ./.venv/etc -> config files
# -> ./.venv/var -> database files
# -> ./.venv/var/log -> access/event logs
# -> ./.venv/Extensions -> external methods
$ ./.venv/bin/mkwsgiinstance -d ./.venv -u admin:admin

# Run the Zope application server in debug mode
$ ./.venv/bin/runwsgi -v ./.venv/etc/zope.ini --debug debug-mode=on
```

### Checkout and link the content models

> [!TIP]
> The following commands demonstrate how to [check out just a single subdirectory from a large Git repository](https://gist.github.com/dinhvle/d085848c09ebd7d3a4a52de9f026c0d3). This sparse checkout is optional.

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
  - **`redis`**: The [Redis](https://redis.io/) in-memory key-value data structure store
    - Image: `docker.io/redis:7.4-alpine`
    - Port: `6379` (mapped to `6379` internally)
    - Used as message broker for background jobs (queue endpoints) and caching (cache endpoints)

## Images

- [**`Dockerfile.zms`**](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.zms): Builds the ZMS content management system.
    - Base: `ghcr.io/idasm-unibe-ch/unibe-cms:python3.14.4-zope6.1`
    - Extras: Installs `zms.unibe` with `msgraphapi` support.
    - [Entrypoint](https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/): Runs the Zope WSGI server via `runwsgi` on port 8080.

- [**`Dockerfile.fastapi`**](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.fastapi): Builds the FastAPI using ZMS headless mode.
    - Base: `docker.io/python:3.14.4`
    - Extras: Installs `zms.unibe` with `fastapi` support.
    - [Entrypoint](https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/): Runs `fastapi dev` on port 8000.

## Configs
- **`configure.zcml`**: Zope Component Architecture registrations and dependencies
- **`site.zcml`**: Zope Component Architecture initialization as main entry point
- **`zodb-relstorage.conf`**: Zope Object Database connection settings for RelStorage
- **`zodb-zeo.conf`**: Zope Object Database connection settings for ZEO
- **`zope.conf`**: Zope Server Settings with directives, policies, etc.
- **`zope.ini`**: Zope Server Configs for wsgi, waitress, waitress.queue, etc.

## License

Copyright (c) 2020-2026 [UniBE, University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).
