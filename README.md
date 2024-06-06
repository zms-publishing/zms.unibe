# UniBE CMSAPI

The implementation of a RESTful API for UniBE CMS relies on the ~~web application (micro)framework Flask~~ [FastAPI](https://fastapi.tiangolo.com) Library. This should enable a more lightweight Python development mode alongside the historically grown Zope stack.

Additionally CMSAPI makes use of ~~Flasgger to generate the documentation~~ [SQLModel](https://sqlmodel.tiangolo.com) to implement the object relational mapping and is served by [Uvicorn](https://www.uvicorn.org) in testing and production deployments.

## Codebase

**REST-API Repositories**
* https://github.com/idasm-unibe-ch/zms-fastapi

## Local container environment

Prerequisites:
- Docker

Execute the following commands to build and run the CMSAPI containers:

```bash
$ docker compose build zms-base
$ docker compose build
$ docker compose up
```

Hint: Everytime you change the code you have to re-execute these commands. You can skip the `docker compose build zms-base` step if `zms-base` didn't change.

Docker compose runs the following containers:
- `api`: `zms-fastapi` container for API queries
- `adm`: `zms-fastapi` container which runs cronjobs
- `zeo`: ZMS data container
- `postgres`: Database container used for API endpoints which contains structured data parsed from ZEO data.
- `doc`: `mkdocs` container including API documentation


## Local Development

[PyCharm](https://www.jetbrains.com/pycharm/) is the recommended IDE for local development. First the desired Python version has to be installed for your system. Second an isolated Python virtual environment has to be created. Third the needed software stack has to be installed and setup.

    $ app/bin/pip install \
        Zope[wsgi]==5.8.6 \
        -c https://zopefoundation.github.io/Zope/releases/5.8.6/constraints.txt \
        -e zms-headless \
        -r requirements.txt \
        -c constraints.txt

A sample run configuration:

    <component name="ProjectRunConfigurationManager">
        <configuration default="false" name="unibe-cmsapi-v3" type="PythonConfigurationType" factoryName="Python">
            <option name="SDK_HOME" value="$PROJECT_DIR$/venvpy310-cmsapi/bin/python" />
            <option name="SCRIPT_NAME" value="uvicorn" />
            <option name="PARAMETERS" value="cmsapi.main:app --port=5003 --reload" />
            <envs>
              <env name="PYTHONUNBUFFERED" value="1" />
            </envs>
            ...
        </configuration>
    </component>

## Container Environments

* Testing: [test-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config-test/browse/stacks/test-unibe-cmsapi/docker-compose.yml) => https://api.cms.test.unibe.ch/v3
* Production: [prod-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config/browse/stacks/prod-unibe-cmsapi/docker-compose.yml) => https://api.cms.unibe.ch/v3
