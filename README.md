# zms.unibe / Add-on Package

### Integrate ZMS with unibe.ch and unibe.app

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

This `zms.unibe` comprehensive Python library extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality and adds [FastAPI](https://fastapi.tiangolo.com) support.

It includes several modules developed to power the [Web/Mobile Platform](https://idasm-unibe-ch.github.io/unibe-web-mobile/) of the University of Bern, [UniBE](https://unibe.ch) in Switzerland – but also a set of [Helper Functions](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md) that can be used as standalone library in any Python project.

## Installation

- [Install from scratch](#install-from-scratch)
  - [Standalone Library with Helper Functions](#standalone-library-with-helper-functions)
  - [ZMS Content Management System based on Zope](#zms-content-management-system-based-on-zope)
  - [FastAPI endpoints using ZMS/Zope in headless mode](#fastapi-endpoints-using-zmszope-in-headless-mode)

## Helper Functions

- see [`EXAMPLES.md`](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md)
  - [Date/Time handling](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#datetime-handling)
  - [Date/Time formatting](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#datetime-formatting)
  - [Output sanitization](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#output-sanitization)
  - [String splitting](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#string-splitting)

## Development Environment

- see [`dev/README.md`](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md)
  - [Overview](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#overview)
  - [Usage](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#usage)
  - [Environment](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#environment)
    - [Start the container environment](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#start-the-container-environment)
    - [Checkout and link the content models](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#checkout-and-link-the-content-models)
  - [Services](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#services)
    - [Compose](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#compose)
    - [Images](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#images)
    - [Configs](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#configs)
  - [License](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md#license)

## Install from scratch

1. Get the `uv` Python package and project manager: https://docs.astral.sh/uv/getting-started/installation/

2. Create a new project with `uv`:
```bash
➜  PyProjects ✗ uv init MyNewProj 
Initialized project `mynewproj` at `/Users/cmeier/PyProjects/MyNewProj`

➜  PyProjects ✗ cd MyNewProj
```

### Standalone Library with Helper Functions

3. Add `zms.unibe` to your project:
```bash
➜  MyNewProj git:(main) ✗ uv add git+https://github.com/zms-publishing/zms.unibe

Using CPython 3.15.1
Creating virtual environment at: .venv
  Updated https://github.com/zms-publishing/zms.unibe (e2467e3a108fd8c983fecd43c7a76d0b99431a99)
Resolved 101 packages in 0.70ms
  Built mynewproj @ file:///Users/cmeier/PyProjects/MyNewProj
  Built zms-unibe @ git+https://github.com/zms-publishing/zms.unibe@e2467e3a108fd8c983fecd43c7a76d0b99431a99
Prepared 99 packages in 4.65s
Installed 99 packages in 155ms
````
<details>
<summary>Details</summary>
<pre>
 + annotated-doc==0.0.5
 + annotated-types==0.8.0
 + anyio==4.15.1
 + anytree==2.13.0
 + arrow==1.4.0
 + asttokens==2.4.1
 + attrs==26.1.0
 + audioop-lts==0.2.2
 + azure-ai-documentintelligence==1.0.2
 + azure-core==1.41.0
 + azure-identity==1.27.0
 + babel==2.18.0
 + beautifulsoup4==4.15.0
 + certifi==2026.10.23
 + cffi==2.1.1
 + chardet==7.7.0
 + charset-normalizer==3.5.2
 + cobble==0.1.4
 + cryptography==50.0.2
 + datetime==6.0
 + defusedxml==0.7.1
 + devtools==0.13.0
 + dnspython==2.9.1
 + email-validator==2.3.0
 + et-xmlfile==2.0.0
 + events==0.5
 + executing==2.3.0
 + ftfy==6.3.1
 + grpcio==1.85.1
 + h11==0.16.0
 + httpcore2==2.16.0
 + httpx2==2.16.0
 + ics==0.7.3
 + idna==3.20
 + isodate==0.7.2
 + jiter==0.18.0
 + lxml==6.1.3
 + mammoth==1.13.0
 + markdown==3.11.2
 + markdown-it-py==4.2.0
 + markdownify==1.2.3
 + markitdown==0.0.2
 + mdurl==0.1.2
 + msal==1.39.0
 + msal-extensions==1.3.1
 + mynewproj==0.1.0 (from file:///Users/cmeier/PyProjects/MyNewProj)
 + numpy==2.5.4
 + oauthlib==4.0.0
 + olefile==0.47
 + openai==3.42.0
 + openpyxl==3.1.5
 + opensearch-protobufs==1.2.0
 + opensearch-py==3.2.0
 + pandas==3.1.0
 + pathvalidate==3.3.1
 + pdfminer-six==20260107
 + pillow==13.0.0
 + protobuf==7.36.2
 + psycopg==3.3.6
 + psycopg-binary==3.3.6
 + psycopg2-binary==2.9.13
 + puremagic==2.2.0
 + pycparser==3.12
 + pydantic==2.14.2
 + pydantic-core==2.50.2
 + pydub==0.25.1
 + pygments==2.21.0
 + pyjwt==2.15.1
 + python-dateutil==3.0.0
 + python-dotenv==1.2.4
 + python-pptx==1.0.2
 + pytz==2026.6
 + requests==2.34.2
 + requests-oauthlib==2.0.0
 + rich==15.0.0
 + shellingham==1.5.4
 + six==1.17.0
 + sniffio==1.3.1
 + soupsieve==3.0.4
 + speechrecognition==3.17.0
 + sqlalchemy==2.1.6
 + sqlmodel==0.0.48
 + standard-aifc==3.13.0
 + standard-chunk==3.13.0
 + tabulate==0.10.0
 + tatsu==5.15.1
 + truststore==0.10.5
 + typer==0.27.3
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
 + tzdata==2026.6
 + urllib3==2.8.0
 + wcwidth==0.9.4
 + xlrd==2.0.2
 + xlsxwriter==3.3.1
 + xmltodict==1.0.4
 + youtube-transcript-api==1.2.4
 + zms-unibe==2026.10.6+e2467e3a108fd8c983fecd43c7a76d0b99431a99 (from git+https://github.com/zms-publishing/zms.unibe@e2467e3a108fd8c983fecd43c7a76d0b99431a99)
 + zope-interface==8.7
</pre>
</details>

4. Test the Helper Functions in your project:
```bash
➜  MyNewProj git:(main) ✗ .venv/bin/python

Python 3.15.1 (main, Oct 21 2026, 17:39:16) [Clang 23.1.3 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from zms.unibe.helpers import *
Helper: zms.unibe.helpers.datetime.local_timezone
Helper: zms.unibe.helpers.datetime.get_when
Helper: zms.unibe.helpers.string.sanitize_html
Helper: zms.unibe.helpers.string.flatten_to_str_list
Helper: zms.unibe.helpers.string.normalize_split_by
>>> get_when()
'2026-10-31T11:13:49+01:00'
```

### ZMS Content Management System based on Zope

5. Add Zope to your project:
```bash
➜  MyNewProj git:(main) ✗ .venv/bin/update-zope-constraints --version 6.3

Updated /Users/cmeier/PyProjects/MyNewProj/pyproject.toml
Used constraints from https://raw.githubusercontent.com/zopefoundation/Zope/6.3/constraints.txt

➜  MyNewProj git:(main) ✗ uv add git+https://github.com/zms-publishing/zms.unibe --extra zope

Resolved 216 packages in 1.66s
  Built mynewproj @ file:///Users/cmeier/PyProjects/MyNewProj
  Built zope-proxy==7.3
  Built zope-container==7.3
  Built zodbpickle==4.5
  Built persistent==6.8
  Built zope-security==8.4
  Built accesscontrol==7.5
  Built btrees==6.5
  Built persistence==5.5
Prepared 115 packages in 12.59s
Uninstalled 1 package in 0.80ms
Installed 116 packages in 109ms
```
<details>
<summary>Details</summary>
<pre>
 + accesscontrol==7.5
 + acquisition==6.4
 + authencoding==6.1
 + btrees==6.5
 - certifi==2026.10.23
 + certifi==2026.10.19
 + chameleon==4.6.0
 + configparser==7.3.0
 + documenttemplate==5.4
 + docutils==0.22.4
 + extensionclass==6.5
 + five-localsitemanager==5.0
 + genshi==0.7.12
 + html5lib==1.1
 + htmldiff2==0.2.2
 + legacy-cgi==2.6.4
 + missing==5.3
 + multimapping==5.1
 + multipart==2.0.1
 ~ mynewproj==0.1.0 (from file:///Users/cmeier/PyProjects/MyNewProj)
 + outcome==1.3.0.post0
 + packaging==26.3
 + paste==3.10.1
 + pastedeploy==3.1.0
 + perfmetrics==4.3.0
 + persistence==5.5
 + persistent==6.8
 + products-btreefolder2==6.0
 + products-cmfcore==3.9
 + products-externalmethod==6.1
 + products-genericsetup==5.2
 + products-mailhost==6.1
 + products-mcdutils==5.1
 + products-pluggableauthservice==4.3
 + products-pluginregistry==3.1
 + products-pythonscripts==5.4
 + products-sessions==6.2
 + products-siteerrorlog==7.0
 + products-standardcachemanagers==6.1
 + products-temporaryfolder==8.1
 + products-zcatalog==7.4
 + products-zodbmountpoint==3.0
 + products-zsqlmethods==5.1
 - pycparser==3.12
 + pycparser==3.11
 + python-gettext==5.0
 + python-memcached==1.62
 - pytz==2026.6
 + pytz==2026.5
 + record==4.2
 + relstorage==4.3.0
 + restrictedpython==8.5
 + roman==5.2
 + ruamel-yaml==0.19.1
 + setuptools==84.2.1
 + sortedcontainers==2.4.0
 + tempstorage==6.0
 + transaction==5.1
 + trio==0.34.0
 + waitress==3.0.2
 + webencodings==0.6.1
 + webob==1.8.11
 + webtest==3.0.7
 + wsgiproxy2==0.5.1
 + z3c-pt==5.2
 + zc-lockfile==4.0
 + zconfig==4.3
 + zdaemon==5.2.1
 + zeo==6.2
 + zexceptions==6.0
 + zms==6.1.0
 + zodb==6.4
 + zodbpickle==4.5
 + zodburi==3.0.0
 + zope==6.3
 + zope-annotation==6.0
 + zope-app-publication==6.0
 + zope-authentication==6.0
 + zope-browser==4.0
 + zope-browsermenu==6.0
 + zope-browserpage==6.0
 + zope-browserresource==6.0
 + zope-cachedescriptors==6.0
 + zope-component==7.1
 + zope-configuration==7.1
 + zope-container==7.3
 + zope-contentprovider==7.0
 + zope-contenttype==6.0
 + zope-datetime==6.0
 + zope-deferredimport==6.1.1
 + zope-deprecation==6.0
 + zope-dottedname==7.1
 + zope-error==6.0
 + zope-event==6.2
 + zope-exceptions==6.0
 + zope-filerepresentation==7.0
 + zope-globalrequest==3.0
 + zope-hookable==8.4
 + zope-i18n==6.0
 + zope-i18nmessageid==8.4
 + zope-lifecycleevent==6.0
 + zope-location==6.0
 + zope-pagetemplate==6.1
 + zope-processlifetime==4.0
 + zope-proxy==7.3
 + zope-ptresource==6.0
 + zope-publisher==8.1
 + zope-schema==8.1
 + zope-security==8.4
 + zope-sendmail==7.3
 + zope-sequencesort==6.0
 + zope-site==6.0
 + zope-size==6.0
 + zope-structuredtext==6.0
 + zope-tal==6.0
 + zope-tales==7.0
 + zope-testbrowser==8.1
 + zope-testing==6.2
 + zope-traversing==6.0
 + zope-untrustedpython==7.0
 + zope-viewlet==6.0
 + zopeundo==6.1
</pre>
</details>

6. Init Zope and run with ZMS:
```bash
➜  MyNewProj git:(main) ✗ ./.venv/bin/mkwsgiinstance -d . -u admin:admin
➜  MyNewProj git:(main) ✗ ./.venv/bin/runwsgi -v ./etc/zope.ini

2026-10-31 10:22:18 INFO [chameleon.config:40][MainThread] directory cache: /Users/cmeier/PyProjects/MyNewProj/var/cache.
...
2026-10-31 10:22:18 INFO [Zope:42][MainThread] Ready to handle requests
Starting server in PID 7067.
2026-10-31 10:22:18 INFO [waitress:449][MainThread] Serving on http://127.0.0.1:8080
```
<details>
<summary>Details</summary>
<pre>
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/jquery/plugin/jquery.plugin.js (Packed: 11317 -> 4774 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/jquery/plugin/jquery.plugin.extensions.js (Packed: 2335 -> 1756 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/zmi.core.js (Packed: 13768 -> 10652 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/zmi.internal.js (Packed: 4725 -> 3173 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/bootstrap/plugin/bootstrap.plugin.zmi.js (Packed: 86877 -> 66577 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/jquery/localstorage/zmi.localstorage.api.js (Packed: 2265 -> 1708 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/zmi.insert.js (Packed: 6564 -> 4396 Bytes)
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/zms-all.min.js.hash
add /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/zmi.js.hash
automated generation of language JavaScript: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/import/_language.yaml
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/ger.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/eng.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/ned.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/fra.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/ita.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/esp.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/chi.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/fas.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/rus.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/hin.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/ara.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/vie.js
generate: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/Products/zms/plugins/www/i18n/heb.js
</pre>
</details>

### FastAPI endpoints using ZMS/Zope in headless mode

7. Add FastAPI to your project:
```bash
➜  MyNewProj git:(main) ✗ uv add git+https://github.com/zms-publishing/zms.unibe --extra fastapi

Resolved 255 packages in 2.02s
Built mynewproj @ file:///Users/cmeier/PyProjects/MyNewProj
Built pyyaml==6.0.3
Prepared 40 packages in 4.21s
Uninstalled 1 package in 1ms
Installed 40 packages in 26ms
```
<details>
<summary>Details</summary>
<pre>
 + agent-detector==2.0.0
 + click==8.5.0
 + croniter==6.2.4
 + detect-installer==0.2.1
 + fastapi==0.162.0
 + fastapi-cache2==0.2.2
 + fastapi-cli==0.0.32
 + fastapi-cloud-cli==0.26.0
 + fastar==0.12.0
 + googleapis-common-protos==1.76.0
 + httpcore==1.0.9
 + httptools==0.9.0
 + httpx==0.28.1
 + jinja2==3.1.6
 + markupsafe==3.0.4
 ~ mynewproj==0.1.0 (from file:///Users/cmeier/PyProjects/MyNewProj)
 + opentelemetry-api==1.45.2
 + opentelemetry-exporter-http-transport==0.66b2
 + opentelemetry-exporter-otlp-common==0.66b2
 + opentelemetry-exporter-otlp-proto-common==1.45.2
 + opentelemetry-exporter-otlp-proto-http==1.45.2
 + opentelemetry-proto==1.45.2
 + opentelemetry-sdk==1.45.2
 + opentelemetry-semantic-conventions==0.66b2
 + pendulum==3.3.0
 + pydantic-extra-types==2.11.1
 + pydantic-settings==2.16.2
 + python-multipart==0.0.32
 + pyyaml==6.0.3
 + redis==8.1.0
 + rich-toolkit==0.20.6
 + rignore==0.8.1
 + rq==3.0.0
 + rq-dashboard-fast==0.9.2
 + sentry-sdk==2.73.0
 + starlette==1.10.0
 + uvicorn==0.54.0
 + uvloop==0.23.0
 + watchfiles==1.3.0
 + websockets==17.4
</pre>
</details>

8. Run FastAPI with Uvicorn:
```bash
➜  MyNewProj git:(main) ✗ .venv/bin/fastapi run --entrypoint zms.unibe.fastapi.app:api --port 5555

 ⚡️ Starting FastAPI in production mode
 🐍 Using import string: zms.unibe.fastapi.app:api
 🌐 Server started at http://0.0.0.0:5555
    Documentation at http://0.0.0.0:5555/docs
  Logs:
 ▕  Started server process [6724]
 ▕  Waiting for application startup.
  ...
  .venv/lib/python3.15/site-packages/zms/unibe/utils/db.py:31 connect_sqldb
    sqlengine: Engine(postgresql://postgres:***@127.0.0.1:5432/unibeportal) (Engine)
 ▕  Application startup complete.
 ▕  Uvicorn running on http://0.0.0.0:5555 (Press CTRL+C to quit)
```
<details>
<summary>Details</summary>
<pre>
FastAPI: Endpoint caching is enabled
Helper: zms.unibe.helpers.datetime.local_timezone
Helper: zms.unibe.helpers.datetime.get_when
Helper: zms.unibe.helpers.string.sanitize_html
Helper: zms.unibe.helpers.string.flatten_to_str_list
Helper: zms.unibe.helpers.string.normalize_split_by
SQLModel: /Users/cmeier/PyProjects/MyNewProj/.venv/lib/python3.15/site-packages/zms/unibe/**/sqlmodels/*.py
SQLModel: zms.unibe.uniaktuell.sqlmodels.UniaktuellArticle
SQLModel: zms.unibe.mobileapp.sqlmodels.NewsEvents
SQLModel: zms.unibe.mobileapp.sqlmodels.ServiceLinks
SQLModel: zms.unibe.datatables.sqlmodels.ZMSDataTable
SQLModel: zms.unibe.datatables.sqlmodels.ZMSBoris
SQLModel: zms.unibe.contacts.sqlmodels.Person
SQLModel: zms.unibe.contacts.sqlmodels.ContactBoxSection
SQLModel: zms.unibe.contacts.sqlmodels.Team
SQLModel: zms.unibe.contacts.sqlmodels.ContactBox
SQLModel: zms.unibe.contacts.sqlmodels.TeamSection
SQLModel: zms.unibe.foundation.sqlmodels.ZMSGraphic
SQLModel: zms.unibe.foundation.sqlmodels.ZMSBase
SQLModel: zms.unibe.foundation.sqlmodels.ZMSDocument
SQLModel: zms.unibe.foundation.sqlmodels.ZMSSite
SQLModel: zms.unibe.foundation.sqlmodels.ZMSFile
SQLModel: zms.unibe.foundation.sqlmodels.ZMSTable
SQLModel: zms.unibe.foundation.sqlmodels.ZMSFolder
SQLModel: zms.unibe.foundation.sqlmodels.ZMSTextarea
SQLModel: zms.unibe.foundation.sqlmodels.CodeBlock
SQLModel: zms.unibe.announcements.sqlmodels.NewsContainer
SQLModel: zms.unibe.announcements.sqlmodels.InfoBox
SQLModel: zms.unibe.announcements.sqlmodels.MediaNews
SQLModel: zms.unibe.announcements.sqlmodels.AlertBox
SQLModel: zms.unibe.announcements.sqlmodels.NewsBox
SQLModel: zms.unibe.teasers.sqlmodels.TeaserContainer2022
SQLModel: zms.unibe.teasers.sqlmodels.TeaserElement2022
SQLModel: zms.unibe.teasers.sqlmodels.Hero2022
SQLModel: zms.unibe.teasers.sqlmodels.Hero
SQLModel: zms.unibe.layouts.sqlmodels.ContentTabs
SQLModel: zms.unibe.layouts.sqlmodels.TwoCols
SQLModel: zms.unibe.layouts.sqlmodels.WeiterbildungStudiengang
SQLModel: zms.unibe.layouts.sqlmodels.ContentPane
SQLModel: zms.unibe.layouts.sqlmodels.UniBEFactsheet
SQLModel: zms.unibe.layouts.sqlmodels.UniBEEvent
SQLModel: zms.unibe.agenda.sqlmodels.ZMSAgenda
SQLModel: zms.unibe.agenda.sqlmodels.AgendaLibraryEN
SQLModel: zms.unibe.agenda.sqlmodels.StatusMessages
SQLModel: zms.unibe.agenda.sqlmodels.AgendaFilemaker
SQLModel: zms.unibe.agenda.sqlmodels.AgendaLibraryDE
SQLModel: zms.unibe.maintenance.sqlmodels.ZMSSchedulerRegistry
SQLModel: zms.unibe.formulator.sqlmodels.ZMSSurveyJSSubmissions
SQLModel: zms.unibe.formulator.sqlmodels.ZMSFormulator
SQLModel: zms.unibe.formulator.sqlmodels.ZMSSurveyJSAttachments
</pre>
</details>

## License

Copyright (c) 2020-2026 [UniBE, University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).