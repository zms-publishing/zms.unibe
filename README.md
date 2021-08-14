# UniBE CMSAPI

The implementation of a RESTful API for UniBE CMS relies on the web application (micro)framework [Flask](https://flask.palletsprojects.com). This should enable a more lightweight Python development mode alongside the historically grown Zope stack.

Additionally CMSAPI makes use of [Flasgger](https://github.com/flasgger/flasgger) to generate the documentation and is served by [Gunicorn](https://gunicorn.org) in testing and production deployments.

## Codebase

**REST-API Repositories**
* Internal Master: https://id-code.unibe.ch/projects/IDCMS/repos/unibe-cmsapi/browse (for deployments)
* External Mirror: https://github.com/id-unibe-ch/unibe-cmsapi (for contributions)

## Local Development

[PyCharm](https://www.jetbrains.com/pycharm/) is the recommended IDE for local development. First the desired Python version has to be installed for your system. Second an isolated Python virtual environment has to be created. Third the needed software stack has to be installed and setup.

Assuming the `unibe-cms` repository has been cloned and a Python virtual environment named `venvpy39-cmsapi` has been created in parallel, the installation steps are:

    (venvpy39-cmsapi) $ bin/pip install -U pip wheel setuptools
    
    (venvpy39-cmsapi) $ bin/pip install Zope[wsgi]==5.3 \
                        -e ../unibe-cmsapi/zms-headless \
                        -c https://zopefoundation.github.io/Zope/releases/5.3/constraints.txt

    (venvpy39-cmsapi) $ bin/pip install -r ../unibe-cms/restapi/requirements-flask.txt \
                        -c https://zopefoundation.github.io/Zope/releases/5.3/constraints.txt

A sample run configuration:

    <component name="ProjectRunConfigurationManager">
        <configuration default="false" name="unibe-cmsapi" type="Python.FlaskServer">
            <option name="SDK_HOME" value="$PROJECT_DIR$/venvpy39-cmsapi/bin/python" />
            <option name="target" value="$PROJECT_DIR$/unibe-cms/restapi/cmsapi/app.py" />
            <option name="targetType" value="PATH" />
            <option name="flaskDebug" value="true" />
            ...
        </configuration>
    </component>

## Container Environments

* Development: [dev-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config-test/browse/stacks/dev-unibe-cmsapi)
* Testing: [test-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config-test/browse/stacks/test-unibe-cmsapi/docker-compose.yml)
* Production:  [prod-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config/browse/stacks/prod-unibe-cmsapi/docker-compose.yml)
