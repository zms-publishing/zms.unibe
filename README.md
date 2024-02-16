# UniBE CMSAPI

The implementation of a RESTful API for UniBE CMS relies on the ~~web application (micro)framework Flask~~ [FastAPI](https://fastapi.tiangolo.com) Library. This should enable a more lightweight Python development mode alongside the historically grown Zope stack.

Additionally CMSAPI makes use of ~~Flasgger to generate the documentation~~ [SQLModel](https://sqlmodel.tiangolo.com) to implement the object relational mapping and is served by [Uvicorn](https://www.uvicorn.org) in testing and production deployments.

## Codebase

**REST-API Repositories**
* Internal Master: https://id-code.unibe.ch/projects/IDCMS/repos/unibe-cmsapi/browse (for deployments)
* External Mirror: https://github.com/id-unibe-ch/unibe-cmsapi (for contributions)

## Local Development

[PyCharm](https://www.jetbrains.com/pycharm/) is the recommended IDE for local development. First the desired Python version has to be installed for your system. Second an isolated Python virtual environment has to be created. Third the needed software stack has to be installed and setup.

    $ app/bin/pip install \
        -e ../unibe-cms/backend/'zope[wsgi]' \
        -c ../unibe-cms/backend/zope/constraints.txt \
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
