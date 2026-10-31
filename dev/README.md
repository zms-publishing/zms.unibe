# zms.unibe / Development Environment

### Integrate ZMS with unibe.ch and unibe.app

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

This `zms.unibe` comprehensive Python library extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality and adds [FastAPI](https://fastapi.tiangolo.com) support.

It includes several modules developed to power the [Web/Mobile Platform](https://idasm-unibe-ch.github.io/unibe-web-mobile/) of the University of Bern, [UniBE](https://unibe.ch) in Switzerland – but also a set of [Helper Functions](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md) that can be used as standalone library in any Python project.

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
- [Environment](#environment)
  - [Start the container environment](#start-the-container-environment)
  - [Checkout and link the content models](#checkout-and-link-the-content-models)
- [Services](#services)
  - [Compose](#compose)
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

This project provides two specialized `Dockerfiles` to support both the legacy [`zope`](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.zope) stack and the modern [`fastapi`](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.fastapi) stack. The `src/zms/unibe/conf/` directory contains essential configuration for the Zope application server.

The [`compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml) file orchestrates a [multi-container environment](https://docs.docker.com/compose/intro/compose-application-model/) for local development. The services use [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) reflecting the changes to local code/configs in the containers instantly and restart the servers automatically.

<details>
<summary>Project Structure</summary>

```
zms.unibe
├── LICENSE
├── README.md
├── pyproject.toml [-> for zms.unibe package installation]
├── Dockerfile.fastapi
├── Dockerfile.zope
├── compose.yaml
├── compose.dev.yaml
├── compose.empty.yaml
├── versions.env 
├── dev
│   ├── .python-version
│   ├── pyproject.toml [-> to bootstrap zms.unibe dev environment]
│   ├── uv.lock
│   ├── README.md
│   └── ... [-> local checkouts in editable mode]
└── src
    └── zms
        └── unibe
            ├── agenda
            │   ├── schemas
            │   └── sqlmodels
            ├── ...
            ├── alembic
            │   ├── versions
            │   ├── alembic.ini
            │   ├── env.py
            │   └── README.md
            ├── conf
            │   ├── zodb-relstorage.conf
            │   ├── zodb-zeo.conf
            │   ├── zope.conf
            │   └── zope.ini
            ├── ...
            ├── fastapi
            │   ├── mobileapp
            │   ├── zmscontent
            │   ├── app.py [-> FastAPI main app]
            │   └── main.py [-> FastAPI sub apps]
            ├── ...
            ├── helpers
            │   ├── DotDict.py
            │   ├── MockDecorator.py
            │   ├── datetime.py
            │   ├── string.py
            │   └── system.py
            ├── ...
            ├── patches
            │   ├── monkey
            │   ├── security
            │   └── configure.zcml
            ├── ...
            ├── tasks
            │   ├── cron_config.py
            │   ├── ...
            │   └── task_config.py
            ├── ...
            └── utils
                ├── zms2sql
                │   ├── cli.py
                │   ├── getters.py
                │   └── tables.py
                ├── zope
                │   ├── context.py
                │   ├── update.py
                │   └── zodb.conf
                ├── db.py
                ├── dependencies.py
                ├── enums.py
                ├── subscribers.py
                └── types.py
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

The package requires [Python 3.12+](https://www.python.org/downloads/) and depends on

- **Application Server**: `Zope`, `Products.PluggableAuthService`, `Products.mcdutils`
- **Database**: `SQLAlchemy`, `SQLModel`, `relstorage`, `psycopg2`, migration with `[alembic]` extra
- **Web/API**: `FastAPI`, `starlette`, `pydantic`, `requests`, `uvicorn` with `[fastapi]` extra
- **Utilities**: `typer`, `rich`, `python-dotenv`, `devtools`, debugger with `[pydevd-pycharm]` extra
- **Office Integration**: `XlsxWriter`, `azure-identity`, `msgraph-sdk` with `[msgraphapi]` extra
- **Data Processing**: `pandas`, `beautifulsoup4`, `lxml`, `MarkItDown`, `rq` with `rq-dashboard-fast`

See [`pyproject.toml`](https://github.com/zms-publishing/zms.unibe/blob/main/pyproject.toml) for the complete list and references of dependencies and `zms.unibe/constraints-Zope-*.txt` for their pinned versions.

</details>

<details>
<summary>Utilities</summary>
<br />

The package provides the `zms2sql` command-line tool for object-relational mappings to mirror selected data from the [ZODB](https://zodb.org) to [PostgreSQL](https://www.postgresql.org), for example:

```bash
$ ./.venv/bin/zms2sql --help
```

Furthermore, it provides the `update-zope-constraints` utility to update the dependencies to the pinned revisions for the specified Zope version in [`dev/pyproject.toml`](https://github.com/zms-publishing/zms.unibe/blob/main/dev/pyproject.toml):

```bash
$ ./.venv/bin/update-zope-constraints --version 6.3
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

## Environment

### Start the container environment

> [!NOTE]
> The base image `ghcr.io/idasm-unibe-ch/unibe-cms` is required to build on top of – permission is required to check it out. In addition, it is expected that the `zeo`, `memcached`, and `psql` containers from the `unibe-cms` stack are running to provide the data storages.

```bash
# Checkout the project
$ git clone https://github.com/zms-publishing/zms.unibe.git

# Checkout the dependencies for editable mode
$ cd dev
$ git clone https://github.com/zopefoundation/Zope.git zope
$ git clone https://github.com/zms-publishing/ZMS.git products-zms

# Force rebuild of the containers
$ docker compose build --no-cache

# Run the containers watching for file changes in defined directories
$ docker compose up --watch
```

These directories are synchronized into the containers - see `develop.watch` in [`compose.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.yaml#L28) and [`compose.dev.yaml`](https://github.com/zms-publishing/zms.unibe/blob/main/compose.dev.yaml)
- Code Sync for `zms.unibe` library
  - Changes in `./src/` to `/app/src`
- Config Sync for Zope application server:
  - Changes in `./src/zms/unibe/conf/` to `/app/dev/etc`
- Editable Dependencies for Zope/ZMS:
  - Changes in `./dev/zope/src` to `/app/dev/zope/src/zope/src`
  - Changes in `./dev/products-zms/Products/zms` to `/app/dev/zope/src/products-zms/Products/zms`

### Checkout and link the content models

> [!TIP]
> The following commands demonstrate how to [check out just a single subdirectory from a large Git repository](https://gist.github.com/dinhvle/d085848c09ebd7d3a4a52de9f026c0d3). This sparse checkout is optional.

> [!NOTE]  
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

### Compose

- **`zms-unibe-dev`**
  - **`zope`**: The Zope/ZMS backend with [zmi](https://zope.readthedocs.io/en/latest/zopebook/UsingZope.html) and [web](https://idasm-unibe-ch.github.io/unibe-web-storybook/) frontend
    - Image: `ghcr.io/idasm-unibe-ch/zms-unibe-dev-zope:local`
    - Port: `8088` (mapped to `8080` internally)
    - Zope/ZMS: [http://127.0.0.1:8088/manage](http://localhost:8088/manage)
  - **`fastapi`**: The FastAPI frontend/API layer
    - Image: `ghcr.io/idasm-unibe-ch/zms-unibe-dev-fastapi:local`
    - Port: `5055` (mapped to `8000` internally)
    - v1: [http://127.0.0.1:5055/v1/docs](http://127.0.0.1:5055/v1/docs) (content and scheduler endpoints)
    - v3: [http://127.0.0.1:5055/v3/docs](http://127.0.0.1:5055/v3/docs) (mobile app endpoints)
  - **`redis`**: The [Redis](https://redis.io/) in-memory key-value data structure store
    - Image: `docker.io/redis:7.4-alpine`
    - Port: `6379` (mapped to `6379` internally)
    - Used as message broker for background jobs (queue endpoints) and caching (cache endpoints)

### Images

- [**`Dockerfile.zope`**](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.zope): Builds the Zope/ZMS content management system.
    - Base: `docker.io/python:3.14.9-slim`
    - Extras: Installs `zms.unibe` with `msgraphapi` support.
    - [Entrypoint](https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/): Runs the Zope WSGI server via `runwsgi` on port 8080.

- [**`Dockerfile.fastapi`**](https://github.com/zms-publishing/zms.unibe/blob/main/Dockerfile.fastapi): Builds the FastAPI using Zope/ZMS headless mode.
    - Base: `docker.io/python:3.14.9-slim`
    - Extras: Installs `zms.unibe` with `fastapi` support.
    - [Entrypoint](https://www.docker.com/blog/docker-best-practices-choosing-between-run-cmd-and-entrypoint/): Runs `fastapi dev` on port 8000.

### Configs
- [**`src/zms/unibe/conf/configure.zcml`**](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/conf/configure.zcml): Zope Component Architecture registrations and dependencies
- [**`src/zms/unibe/conf/site.zcml`**](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/conf/site.zcml): Zope Component Architecture initialization as main entry point
- [**`src/zms/unibe/conf/zodb-relstorage.conf`**](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/conf/zodb-relstorage.conf): Zope Object Database connection settings for RelStorage
- [**`src/zms/unibe/conf/zodb-zeo.conf`**](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/conf/zodb-zeo.conf): Zope Object Database connection settings for ZEO
- [**`src/zms/unibe/conf/zope.conf`**](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/conf/zope.conf): Zope Server Settings with directives, policies, etc.
- [**`src/zms/unibe/conf/zope.ini`**](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/conf/zope.ini): Zope Server Configs for wsgi, waitress, waitress.queue, etc.

## License

Copyright (c) 2020-2026 [UniBE, University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).