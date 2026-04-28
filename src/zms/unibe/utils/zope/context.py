import pathlib
import os
import Zope2
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.users import system as user
from Testing.makerequest import makerequest
from Zope2.Startup.run import make_wsgi_app
from zope.globalrequest import setRequest
from fastapi import HTTPException

zope_conf_path = pathlib.Path(__file__).parent.joinpath('zope.conf').resolve()
_zope_initialized = False

def create_zope_app_context():
    """
    Initializes Zope, creates a new DB connection, adds an HTTPRequest
    at app.REQUEST and returns app.unibe.content (ZMS context).

    This method should be called once per client request in multi-threaded
    applications (e.g. web applications). This way each client request will get
    a separate request object and will have a separate connection.

    Important: The setRequest method is thread-local.
    Therefore this method should be called only once per thread to avoid
    parallel alterations of the global request object which would lead to
    inconsistent results.
    """
    global _zope_initialized
    if not _zope_initialized:
        if not zope_conf_path.is_file():
            setup_conf()
        make_wsgi_app({}, zope_conf_path.as_posix())
        _zope_initialized = True
    # Create new DB connection: app = connection.root()['Application'] (OFS.Application.Application)
    app = Zope2.app()
    # Add an HTTPRequest at app.REQUEST
    app = makerequest(app)
    app.REQUEST['PARENTS'] = [app]
    app.REQUEST.set('ZMS_CONTEXT_URL', True)
    setRequest(app.REQUEST)
    newSecurityManager(None, user)
    return app

def get_zmsindex(portal_master, context):
    
    def traverse(pth, ctx, site=None):
        for p in pth:
            if p in ctx:
                pth.remove(p)
                if pth:
                    site = traverse(pth, ctx[p], site)
                elif 'content' in ctx[p] and 'zcatalog_index' in ctx[p]:
                    return ctx[p]['zcatalog_index']
        return site

    path = [x for x in str(portal_master).split('/') if x not in ('', 'content')]
    zmsindex = traverse(path, context)
    if not zmsindex:
        raise HTTPException(status_code=404,
                            detail=f"Portal master '{portal_master}' not found.")
    return zmsindex

def setup_conf():
    print('Setup zope.conf')
    zope_conf_template_path = pathlib.Path(__file__).parent.joinpath('zope.conf.template').resolve()
    with open(zope_conf_template_path) as f:
        config = f.read()
    config = config.replace('{{ ZEO_URL }}', os.environ.get('ZEO_URL', '127.0.0.1:8000'))
    with open(zope_conf_path, 'w') as f:
        f.write(config)
    