# UniBE CMSAPI

The implementation of a RESTful API for UniBE CMS relies on the web application (micro)framework [Flask](https://flask.palletsprojects.com). This should enable a more lightweight Python development mode alongside the historically grown Zope stack.

Additionally CMSAPI makes use of [Flasgger](https://github.com/flasgger/flasgger) to generate the documentation and is served by [Gunicorn](https://gunicorn.org) in testing and production deployments.

## Codebase

**REST-API repository (internal)**
* https://id-code.unibe.ch/projects/IDCMS/repos/unibe-cmsapi/browse

## Development

[PyCharm](https://www.jetbrains.com/pycharm/) is the recommended IDE for local development. First the desired Python version has to be installed for your system. Second an isolated Python virtual environment has to be created. Third the needed software stack has to be installed and setup.

Assuming the `unibe-cms` repository has been cloned and a Python virtual environment named `venvpy39-cmsapi` has been created in parallel, the installation steps are:

    (venvpy39-cmsapi) $ bin/pip install -U pip wheel setuptools
    
    (venvpy39-cmsapi) $ bin/pip install Zope[wsgi]==5.1.2 \
                        -e ../unibe-cmsapi/zms-headless \
                        -c https://zopefoundation.github.io/Zope/releases/5.1.2/constraints.txt

    (venvpy39-cmsapi) $ bin/pip install -r ../unibe-cms/restapi/requirements-flask.txt \
                        -c https://zopefoundation.github.io/Zope/releases/5.1.2/constraints.txt

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

## Environments

### Testing

* `CMSTEST3` see current [deployment script](https://id-code.unibe.ch/projects/IDCMS/repos/unibe-cms/browse/bin/zms.deployZMSunibe.cmstest3#90)
* `TODO` integrate into [docker-config-test](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config-test/browse)

### Production

* `TODO` integrate into [docker-config](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config/browse)
