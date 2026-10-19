# invoked by etc/site.zcml applying src/zms/unibe/patches/configure.zcml
# <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
import os
from Products.zms.standard import pybool

try:
    # initialize monkey patches on zope startup
    from zms.unibe.patches.monkey import ExternalMethod_always_reloadIfChanged
    from zms.unibe.patches.monkey import MemCached_log_instead_raise_ConnectionError

    if pybool(os.getenv('ZMS_UV_PACKAGE_MANAGER')):
        from .monkey import Products_zms_standard_get_installed_packages

    # initialize security assertions on zope startup
    from zms.unibe.patches.security import assertions

    from App.config import getConfiguration
    if getConfiguration().debug_mode:
        # allow debugging in Restricted Python
        print("Debug: import pdb; pdb.set_trace() allowed in Restricted Python")
        from AccessControl import allow_module
        allow_module('pdb')
    
except Exception as e:
    print(f"Ignore: {e} in zms.unibe.patches")
