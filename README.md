# zms.unibe 2.0

## Python-based extensions for and integrations with the ZMS publishing system

This `zms.unibe` add-on package is a comprehensive library that extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality with generally applicable features and utilities as well as integrations specific for [UniBE](https://unibe.ch). It includes modules for agenda management, announcements, contacts, data tables, forms and surveys, layouts, mobile app support, and more.

It features a headless RESTful API for accessing the content objects stored in [ZODB](https://zodb.org) and uses the ~~web application (micro)framework Flask~~ [FastAPI](https://fastapi.tiangolo.com) framework, which is served by [Uvicorn](https://www.uvicorn.org). Additionally, it relies on ~~Flasgger to generate the documentation~~ [SQLModel](https://sqlmodel.tiangolo.com) for implementing an object-relational mapping.

This solution architecture, based on modern [Python](https://www.python.org) frameworks, unlocks a more lightweight development mode alongside the historically grown Zope stack.

## Repository
- https://github.com/zms-publishing/zms.unibe
- https://github.com/zms-publishing/zms.unibe/releases

## Setup development sandbox

### With [FastAPI](https://fastapi.tiangolo.com) Support

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

```bash
$ git clone https://github.com/zms-publishing/zms.unibe.git
$ virtualenv .venv
$ ./.venv/bin/pip install -e ./'zms.unibe[fastapi]'
$ ./.venv/bin/fastapi dev  # -> http://127.0.0.1:8000/v1
                           # -> http://127.0.0.1:8000/v3
```

### Include [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/overview) Support

Microsoft Graph is the gateway to data and intelligence in Microsoft cloud services like [Microsoft Entra](https://learn.microsoft.com/en-us/graph/identity-network-access-overview) and [Microsoft 365](https://learn.microsoft.com/en-us/graph/overview).

```bash
$ ./.venv/bin/pip install -e ./'zms.unibe[msgraphapi]'
```

### Include [Remote Debugging with PyCharm](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html) Support

With [PyCharm](https://www.jetbrains.com/pycharm/) you can debug your application using an interpreter that is located on the other computer, for example, on a web server or dedicated test machine.

```bash
$ ./.venv/bin/pip install -e ./'zms.unibe[pydevd-pycharm]'
```

### Command-Line Tools

The package provides the `zms2sql` command-line utility for object-relational mappings to mirror selected data from the [ZODB](https://zodb.org) to [PostgreSQL](https://www.postgresql.org), for example.

```bash
$ ./.venv/bin/zms2sql --help
```

### Monkey Patches and Helper Utilities

To apply the [monkey patches](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/patches/monkey) for customizing other installed packages as well as the [security assertions](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/patches/security) for using the helper utilities in [RestrictedPython](https://github.com/zopefoundation/RestrictedPython) code (py, zpt, dtml) edited via the web with [ZMI](https://zope.readthedocs.io/en/latest/zopebook/UsingZope.html) or synchronized via the [ZMSRepositoryManager](https://github.com/zms-publishing/ZMS/tree/main/Products/zms/zpt/ZMSRepositoryManager), the following package include must be added to the `./.venv/etc/site.zcml` file:

```xml
<include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
```

## Features

### Integrations with other services
- [DataTables.net](https://datatables.net) samples
- [BORIS](https://boris.unibe.ch) connector
- Outlook connector for [calendar integration via Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/resources/calendar-overview?view=graph-rest-1.0)
- Agenda bridge for flexible data aggregation
- Event schemas and SQL models
- Library and news integration
- IT status messages
- Form management based on [JSON Editor](https://github.com/json-editor/json-editor) 
- [SurveyJS](https://surveyjs.io) integration

### Utilities & custom monkey patches
- Database utilities
- Helper functions
- Enums and context management
- Scheduler registry
- `zms2sql` command-line tool
- `MemCached` error handling
- `ExternalMethod` auto-reload
- Security assertions

### Content object handling
- Base models (ZMSBase, ZMSSite, ZMSFolder, ZMSDocument)
- File and graphic handling
- Tables and text areas
- Code blocks
- Hero components
- Teaser containers and elements
- Content panes and tabs
- Two-column layouts
- Event and factsheet layouts
- Alert boxes, info boxes, news boxes
- Media news and Article management
- Contact boxes and sections
- Persons and Team sections

## Dependencies

The package requires [Python 3](https://www.python.org/downloads/) and depends on:

- **Application Server**: `Zope`, `Products.mcdutils`, `Products.PluggableAuthService`
- **Database**: `SQLAlchemy`, `SQLModel`, `psycopg2`
- **Web/API**: `FastAPI`, `starlette`, `pydantic`, `requests`
- **Data Processing**: `pandas`, `beautifulsoup4`, `lxml`, `MarkItDown`
- **Office Integration**: `XlsxWriter`, `azure-identity`, `msgraph-sdk` with `[msgraphapi]` extra
- **Utilities**: `typer`, `rich`, `python-dotenv`, `devtools`
- **Optional**: `uvicorn` with `[fastapi]` extra

See [`pyproject.toml`](https://github.com/zms-publishing/zms.unibe/blob/main/pyproject.toml) for the complete list and references of dependencies and [`constraints.txt`](https://github.com/zms-publishing/zms.unibe/blob/main/constraints.txt) for their pinned versions.

## Structure

```
zms.unibe
├── README.md
├── Dockerfile
├── docker-compose.yml
├── constraints.txt
├── pyproject.toml
└── src
    └── zms
        └── unibe
            ├── agenda
            │   ├── schemas
            │   └── sqlmodels
            ├── announcements
            │   ├── schemas
            │   └── sqlmodels
            ├── contacts
            │   └── sqlmodels
            ├── datatables
            │   ├── samples
            │   │   ├── agenda
            │   │   ├── announcement
            │   │   ├── ikim
            │   │   ├── kirchenbautag
            │   │   ├── pariscms
            │   │   ├── siteoverview
            │   │   ├── sozinno
            │   │   ├── tree
            │   │   └── webinare
            │   └── sqlmodels
            ├── fastapi
            │   ├── mobileapp
            │   └── zmscontent
            ├── formulator
            │   └── sqlmodels
            ├── foundation
            │   └── sqlmodels
            ├── layouts
            │   └── sqlmodels
            ├── maintenance
            │   └── sqlmodels
            ├── mobileapp
            │   ├── schemas
            │   └── sqlmodels
            ├── patches
            │   ├── monkey
            │   └── security
            ├── teasers
            │   └── sqlmodels
            ├── uniaktuell
            │   ├── schemas
            │   └── sqlmodels
            └── utils
                ├── zms2sql
                ├── zope
                ├── db.py
                ├── enums.py
                └── helpers.py
```

## License

Copyright (c) 2020-2026 [University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).