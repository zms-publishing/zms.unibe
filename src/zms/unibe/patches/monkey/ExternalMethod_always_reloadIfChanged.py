from Products.ExternalMethod.ExternalMethod import ExternalMethod
import os, sys

"""
Load changes from filesystem even if not in debug mode. So changes to files 
initiated by one cluster node will be propagated to other cluster nodes
sharing a common mounted extensions folder.
"""

print('Monkeypatch: Products.ExternalMethod.getFuncDefaults')
def getFuncDefaults(self):
    self.reloadIfChanged()
    if not hasattr(self, '_v_func_defaults'):
        self._v_f = self.getFunction()
    return self._v_func_defaults

ExternalMethod.getFuncDefaults = getFuncDefaults

print('Monkeypatch: Products.ExternalMethod.getFuncCode')
def getFuncCode(self):
    self.reloadIfChanged()
    if not hasattr(self, '_v_func_code'):
        self._v_f = self.getFunction()
    return self._v_func_code

ExternalMethod.getFuncCode = getFuncCode

print('Monkeypatch: Products.ExternalMethod.__call__')
def __call__(self, *args, **kw):
    """Call an ExternalMethod

    Calling an External Method is roughly equivalent to calling
    the original actual function from Python.  Positional and
    keyword parameters can be passed as usual.  Note however that
    unlike the case of a normal Python method, the "self" argument
    must be passed explicitly.  An exception to this rule is made
    if:

    - The supplied number of arguments is one less than the
      required number of arguments, and

    - The name of the function\'s first argument is 'self'.

    In this case, the URL parent of the object is supplied as the
    first argument.
    """
    filePath = self.filepath()
    if filePath is None:
        raise RuntimeError('external method could not be called '
                           'because it is None')

    if not os.path.exists(filePath):
        raise RuntimeError('external method could not be called '
                           'because the file does not exist')

    self.reloadIfChanged()

    if hasattr(self, '_v_f'):
        f = self._v_f
    else:
        f = self.getFunction()

    __traceback_info__ = args, kw, self._v_func_defaults

    try:
        return f(*args, **kw)
    except TypeError as v:
        tb = sys.exc_info()[2]
        try:
            if ((self._v_func_code.co_argcount -
                 len(self._v_func_defaults or ()) - 1 == len(args)) and
                    self._v_func_code.co_varnames[0] == 'self'):
                return f(self.aq_parent.this(), *args, **kw)

            raise TypeError(v)
        finally:
            tb = None  # NOQA

ExternalMethod.__call__ = __call__
