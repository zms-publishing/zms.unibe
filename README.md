# zms.unibe / Add-on Package

### Integrate ZMS with unibe.ch and unibe.app

- <https://github.com/zms-publishing/zms.unibe>
- <https://github.com/zms-publishing/zms.unibe/releases>

This `zms.unibe` comprehensive library extends [ZMS](https://github.com/zms-publishing/ZMS) and the underlying [Zope](https://github.com/zopefoundation/Zope) functionality.

It includes several modules specific for the [University of Bern (UniBE)](https://unibe.ch) in Switzerland – as well as a set of [helper functions](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md) that can be useful in `Page Templates` or `Python Scripts` in any ZMS/Zope-based CMS.

## Installation

This example assumes you have a working ZMS/Zope installation in a virtual environment.

```bash
$ cd /path/to/your/virtualenv
$ ./bin/pip install "zms.unibe @ git+https://github.com/zms-publishing/zms.unibe.git"

# add to ./etc/site.zcml
<configure xmlns:zcml="http://namespaces.zope.org/zcml">
  <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
</configure>
```

## Helper Functions

- [Code Examples](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md)
  - [Date/Time handling](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#datetime-handling)
  - [Date/Time formatting](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#datetime-formatting)
  - [Output sanitization](https://github.com/zms-publishing/zms.unibe/blob/main/EXAMPLES.md#output-sanitization)

## Development Environment

- see [`dev/README.md`](https://github.com/zms-publishing/zms.unibe/blob/main/dev/README.md)

## License

Copyright (c) 2020-2026 [University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).