# UniBE CMSAPI

The implementation of a RESTful API for UniBE CMS relies on the web application (micro)framework [Flask](https://flask.palletsprojects.com). This should enable a more lightweight Python development mode alongside the historically grown Zope stack.

Additionally CMSAPI makes use of [Flasgger](https://github.com/flasgger/flasgger) to generate the documentation and is served by [Gunicorn](https://gunicorn.org) in testing and production deployments.

## Codebase

**REST-API Repositories**
* Internal Master: https://id-code.unibe.ch/projects/IDCMS/repos/unibe-cmsapi/browse (for deployments)
* External Mirror: https://github.com/id-unibe-ch/unibe-cmsapi (for contributions)

## Local Development

[PyCharm](https://www.jetbrains.com/pycharm/) is the recommended IDE for local development. First the desired Python version has to be installed for your system. Second an isolated Python virtual environment has to be created. Third the needed software stack has to be installed and setup.

Assuming the `unibe-cmsapi` repository has been cloned and a Python virtual environment named `venvpy310-cmsapi` has been created in parallel, the installation steps are:

    (venvpy310-cmsapi) $ bin/pip install -U pip wheel setuptools
    
    (venvpy310-cmsapi) $ bin/pip install Zope[wsgi]==5.5.2 \
                        -e ../unibe-cmsapi/zms-headless \
                        -c https://zopefoundation.github.io/Zope/releases/5.5.2/constraints.txt

    (venvpy310-cmsapi) $ bin/pip install -r ../unibe-cmsapi/requirements-flask.txt \
                        -c https://zopefoundation.github.io/Zope/releases/5.5.2/constraints.txt

A sample run configuration:

    <component name="ProjectRunConfigurationManager">
        <configuration default="false" name="unibe-cmsapi" type="Python.FlaskServer">
            <option name="SDK_HOME" value="$PROJECT_DIR$/venvpy310-cmsapi/bin/python" />
            <option name="target" value="$PROJECT_DIR$/unibe-cmsapi/cmsapi/app.py" />
            <option name="targetType" value="PATH" />
            <option name="flaskDebug" value="true" />
            ...
        </configuration>
    </component>

## Container Environments

* Testing: [test-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config-test/browse/stacks/test-unibe-cmsapi/docker-compose.yml) (standalone stack) => https://api.uniapp-backend.test.unibe.ch/cms/
* Production: [prod-unibe-cmsapi](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config/browse/stacks/prod-unibe-cmsapi/docker-compose.yml) (standalone stack) => https://api.uniapp-backend.unibe.ch/cms/

**Proof of concept (PoC)**

* Kemp4CMS: [test-unibe-cms_api](https://id-code.unibe.ch/projects/EPDOCKER/repos/docker-config-test/browse/stacks/test-unibe-cms/docker-compose.yml#80) (service in stack) => https://api.cms.test.unibe.ch
[`IDCMS-630`](https://idjira.unibe.ch/browse/IDCMS-630) Kemp as Load Balancer / HTTPS / Virtual Hosting / Cluster networking
