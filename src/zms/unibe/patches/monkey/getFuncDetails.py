from Products.ExternalMethod.ExternalMethod import ExternalMethod

print('Monkeypatch: Products.ExternalMethod.getFuncDefaults')
"""
Load changes from filesystem even if not in debug mode. So changes to files 
initiated by one cluster node will be propagated to other cluster nodes
sharing a common mounted extensions folder.
"""

def getFuncDefaults(self):
    # if getConfiguration().debug_mode:
    self.reloadIfChanged()
    if not hasattr(self, '_v_func_defaults'):
        self._v_f = self.getFunction()
    return self._v_func_defaults

ExternalMethod.getFuncDefaults = getFuncDefaults
