# zms-addons

Python-based extensions for and integrations with the [ZMS publishing](https://github.com/zms-publishing/ZMS) system at [UniBE](https://unibe.ch) (University of Bern).

The included `zms.unibe` add-on package is a comprehensive library that extends ZMS and underlying [Zope](https://github.com/zopefoundation/Zope) functionality with institution-specific features, integrations, and utilities. It includes modules for agenda management, announcements, contacts, data tables, forms, layouts, mobile app support, and more.

## Repository
- https://github.com/idasm-unibe-ch/zms-addons
- https://github.com/idasm-unibe-ch/zms-addons/releases

## Setup development sandbox

### From Source

```bash
$ git clone https://github.com/idasm-unibe-ch/zms-addons.git
$ virtualenv .venv
$ ./.venv/bin/pip install -e ./'zms-addons'
```

### With [FastAPI](https://fastapi.tiangolo.com) Support

```bash
$ ./.venv/bin/pip install -e ./'zms-addons[fastapi]'
```

### With [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/overview) Support

```bash
$ ./.venv/bin/pip install -e ./'zms-addons[msgraphapi]'
```

### With [PyCharm Remote Debugging](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html) Support

```bash
$ ./.venv/bin/pip install -e ./'zms-addons[pydevd-pycharm]'
```

### Command-Line Tools

The package provides the `zms2sql` command-line utility for object-relational mappings to mirror selected data in the [ZODB](https://zodb.org) to e.g. [PostgreSQL](https://www.postgresql.org):

```bash
$ ./.venv/bin/zms2sql --help
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
- Hero 2022 components
- Teaser containers and elements
- Content panes and tabs
- Two-column layouts
- Event and factsheet layouts
- Alert boxes, info boxes, news boxes
- Media news and Article management
- Contact boxes and sections
- Person and team management
- Team sections

## Dependencies

The package requires [Python 3](https://www.python.org/downloads/) and depends on, e.g.:

- **Application Server**: `Zope`, `Products.mcdutils`, `Products.PluggableAuthService`
- **Database**: `SQLAlchemy`, `SQLModel`, `psycopg2`
- **Web/API**: `FastAPI`, `starlette`, `pydantic`, `requests`, `msgraph-sdk`
- **Data Processing**: `pandas`, `beautifulsoup4`, `lxml`, `Markdown`
- **Office Integration**: `azure-identity`, `msgraph-sdk`, `XlsxWriter`
- **Utilities**: `typer`, `rich`, `python-dotenv`, `devtools`
- **Optional**: `uvicorn` (with `[fastapi]` extra)

See [`requirements.txt`](https://github.com/idasm-unibe-ch/zms-addons/blob/main/requirements.txt) for the complete list and references of dependencies and [`constraints.txt`](https://github.com/idasm-unibe-ch/zms-addons/blob/main/constraints.txt) for their pinned versions.

## Project Structure

```
zms-addons
├── README.md
├── constraints.txt
├── pyproject.toml
└── src
    └── zms
        └── unibe
            ├── agenda
            │   ├── schemas
            │   └── sqlmodels
            ├── announcements
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
            ├── formulator
            │   └── sqlmodels
            ├── foundation
            │   └── sqlmodels
            ├── layouts
            │   └── sqlmodels
            ├── maintenance
            │   └── sqlmodels
            ├── mobileapp
            │   └── sqlmodels
            ├── patches
            │   ├── monkey
            │   └── security
            ├── teasers
            │   └── sqlmodels
            ├── uniaktuell
            │   └── sqlmodels
            └── utils
                ├── zms2sql
                ├── zope
                └── helpers.py
```
