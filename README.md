# zms.unibe / Add-on Package

### Integrate ZMS with unibe.ch and unibe.app

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

This `zms.unibe` comprehensive Python library extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality.

It includes several modules specific for the [UniBE, University of Bern](https://unibe.ch) in Switzerland – as well as a set of [helper functions](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md) that can be useful in `Page Templates` or `Python Scripts` in any ZMS/Zope-based CMS.

## Installation

These instructions assume you have [Python](https://www.python.org/downloads/) > 3.11 installed.

Using as Standalone Library to access the [Helper Functions](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md):
```bash
$ ./bin/pip install "zms.unibe @ git+https://github.com/zms-publishing/zms.unibe.git"
```
Install and run ZMS content management system based on Zope application server:
```bash
$ cd /path/to/your-project
$ python3 -m venv .venv
$ ./.venv/bin/pip install "zms.unibe[zope] @ git+https://github.com/zms-publishing/zms.unibe.git" \
  -c https://raw.githubusercontent.com/zms-publishing/zms.unibe/main/constraints.txt
$ ./.venv/bin/mkwsgiinstance -d . -u admin:admin 
$ ./.venv/bin/runwsgi -v ./etc/zope.ini
```

## Helper Functions

- [Code Examples](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md)
  - [Date/Time handling](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#datetime-handling)
  - [Date/Time formatting](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#datetime-formatting)
  - [Output sanitization](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#output-sanitization)

## Development Environment

- see [`dev/README.md`](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md)

## License

Copyright (c) 2020-2026 [UniBE, University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).