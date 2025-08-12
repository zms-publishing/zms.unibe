# invoked by etc/site.zcml applying src/zms/unibe/patches/configure.zcml
# <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />

try:
    # initialize monkey patches on zope startup
    from zms.unibe.patches.monkey import ExternalMethod_always_reloadIfChanged
    from zms.unibe.patches.monkey import MemCached_log_instead_raise_ConnectionError

    # initialize security assertions on zope startup
    from zms.unibe.patches.security import assertations
except Exception as e:
    print("ERROR [zms.unibe.patches]:", e)
