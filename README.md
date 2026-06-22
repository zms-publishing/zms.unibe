# zms.unibe 2026+

### Python-based extensions to integrate ZMS with unibe.ch and unibe.app

This `zms.unibe` add-on package is a comprehensive library that extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality with generally applicable features and utilities as well as integrations specific for [UniBE](https://unibe.ch). It includes modules for agenda management, announcements, contacts, data tables, forms and surveys, layouts, mobile app support, and more.

It features a fully decoupled, [headless RESTful API](https://idasm-unibe-ch.github.io/unibe-web-mobile/CMSAPI/) for accessing the content objects stored in [ZODB](https://zodb.org), using the ~~web application (micro)framework Flask~~ [FastAPI](https://fastapi.tiangolo.com) framework, which is served by [Uvicorn](https://www.uvicorn.dev). In addition, it relies on ~~Flasgger to generate the documentation~~ [SQLModel](https://sqlmodel.tiangolo.com) for implementing an object-relational mapping.

Furthermore, it can connect to [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/overview) as the gateway to data and intelligence in Microsoft cloud services like [M365](https://learn.microsoft.com/en-us/graph/overview) or [Entra](https://learn.microsoft.com/en-us/graph/identity-network-access-overview) if the `[msgraphapi]` extra has been applied on installation.

This solution architecture, based on modern [Python](https://www.python.org) frameworks, unlocks a more lightweight development mode alongside the historically grown Zope stack.

<img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/zms6.png" width="33%" /> <img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/fastapi1.png" width="33%" /> <img src="https://raw.githubusercontent.com/zms-publishing/zms.unibe/assets/fastapi3.png" width="33%" />

## Repository

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

## Development

- see [`dev/README.md`](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md)

## Features

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

## Dependencies

### The package requires [Python 3.11+](https://www.python.org/downloads/) and depends on

- **Application Server**: `Zope`, `Products.PluggableAuthService`, `Products.mcdutils`
- **Database**: `SQLAlchemy`, `SQLModel`, `psycopg2`
- **Web/API**: `FastAPI`, `starlette`, `pydantic`, `requests`, `uvicorn` with `[fastapi]` extra
- **Utilities**: `typer`, `rich`, `python-dotenv`, `devtools`, debugger with `[pydevd-pycharm]` extra
- **Office Integration**: `XlsxWriter`, `azure-identity`, `msgraph-sdk` with `[msgraphapi]` extra
- **Data Processing**: `pandas`, `beautifulsoup4`, `lxml`, `MarkItDown`

See [`pyproject.toml`](https://github.com/zms-publishing/zms.unibe/blob/main/pyproject.toml) for the complete list and references of dependencies and [`constraints.txt`](https://github.com/zms-publishing/zms.unibe/blob/main/constraints.txt) for their pinned versions.

### Utilities

The package provides the `zms2sql` command-line tool for object-relational mappings to mirror selected data from the [ZODB](https://zodb.org) to [PostgreSQL](https://www.postgresql.org), for example:

```bash
$ ./.venv/bin/zms2sql --help
```

To apply the [monkey patches](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/patches/monkey) for customizing other installed packages as well as the [security assertions](https://github.com/zms-publishing/zms.unibe/blob/main/src/zms/unibe/patches/security) for using the helper utilities in [RestrictedPython](https://github.com/zopefoundation/RestrictedPython) code (py, zpt, dtml), the following package include must be added to the `./.venv/etc/site.zcml` file:

```xml
<include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
```

This allows editing via the web using [ZMI](https://zope.readthedocs.io/en/latest/zopebook/UsingZope.html) or synchronize code changes via the [ZMSRepositoryManager](https://github.com/zms-publishing/ZMS/tree/main/Products/zms/zpt/ZMSRepositoryManager/readme.md).

To enable support for [Remote Debugging with PyCharm](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html) you can include the `[pydevd-pycharm]` extra on installation.

## Structure

```
zms.unibe
├── LICENSE
├── README.md
├── pyproject.toml
├── constraints.txt
├── Dockerfile.fastapi
├── Dockerfile.zms
├── compose.yaml
├── app
├── cron
│   ├── [scheduled jobs]
│   └── ...
├── conf
│   ├── [local config files]
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
            │   └── zmscontent
            ├── ...
            ├── patches
            │   ├── monkey
            │   └── security
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
