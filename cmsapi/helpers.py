import glob
import importlib.util
import inspect
import sys
import os
from enum import Enum

PATH = os.path.abspath(os.path.dirname(__file__))
PATH = PATH.startswith('/app') and PATH + '/..' or PATH + '/../../unibe-cms'

ZMS_METAS_PATH = f'{PATH}/frontend/ZMSModels/*/*/metaobj_manager/__metas__.py'
ZMS_MODEL_PATH = f'{PATH}/frontend/ZMSModels/*/*/metaobj_manager/*/*/__init__.py'
ZMS_MODEL_ATTR = {}


class AttrType(str, Enum):
    all = "*"
    url = "url"
    image = "image"
    string = "string"
    select = "select"
    boolean = "boolean"
    integer = "int"
    floating = "float"
    datetime = "datetime"


class MetaObj(str, Enum):
    ZMSFolder = "ZMSFolder"
    ZMSDocument = "ZMSDocument"
    ZMSFormulator = "ZMSFormulator"
    ZMSGraphic = "ZMSGraphic"
    newsbox = "newsbox"
    teaser_element_2022 = "teaser_element_2022"


def get_zms_model(name=None, types=('*',), metas=True):

    global ZMS_MODEL_ATTR
    ZMS_MODEL_ATTR = {}

    if metas:
        for module_path in glob.glob(ZMS_METAS_PATH):
            module_name = module_path.rsplit('/', 2)[1]
            _inspect_module(module_name, module_path, types)

    if name is not None:
        for module_path in glob.glob(ZMS_MODEL_PATH):
            module_name = module_path.rsplit('/', 2)[1]
            if name == module_name:
                _inspect_module(module_name, module_path, types)
                break

    return ZMS_MODEL_ATTR


def _inspect_module(module_name, module_path, types):
    global ZMS_MODEL_ATTR

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    for name, cls in inspect.getmembers(sys.modules[module_name]):
        if inspect.isclass(cls):
            try:
                subcls = cls.Attrs
            except AttributeError:
                subcls = cls.Metas
            for attrs in dir(subcls):
                if not attrs.startswith('__'):
                    attr = getattr(subcls, attrs)
                    if attr['type'] in ZMS_MODEL_ATTR:
                        continue  # type already found in metas
                    if attr['type'] in types or '*' in types:
                        ZMS_MODEL_ATTR[attr["id"]] = attr


def parse_subdomain(domain):
    if domain is None:
        domain = ''
    rtn = domain.replace('.cmstest1', '').replace('www.unibe.ch', 'portal')
    return rtn.replace('www.', '').replace('.unibe.ch', '')
