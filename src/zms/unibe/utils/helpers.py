import os
import re
import requests
import time
from devtools import debug
from datetime import datetime, timedelta
from DateTime import DateTime  # legacy Zope implementation, returned e.g. by ZopeTime()
from uuid import UUID

import pytz
from AccessControl import ModuleSecurityInfo
from Products.zms import standard, _blobfields

from .enums import SiteType

security = ModuleSecurityInfo('zms.unibe.utils.helpers.local_timezone')  # allow module import in RestrictedPython


class DotDict(dict):
    """
    https://stackoverflow.com/questions/13520421/recursive-dotdict

    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


print('Addon: zms.unibe.utils.helpers.local_timezone')
@security.public
def local_timezone(dt=None, tz='Europe/Zurich', days_delta=0):
    if dt is None:
        dt = datetime.now()
    elif isinstance(dt, time.struct_time):
        dt = standard.format_datetime_iso(dt)
    elif isinstance(dt, DateTime):  # legacy Zope implementation, returned e.g. by ZopeTime()
        dt = dt.ISO8601()
    try:
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        elif isinstance(dt, int) or isinstance(dt, float):
            dt = datetime.fromtimestamp(dt)
    except (ValueError, TypeError):
        dt = datetime.fromtimestamp(0)  # datetime.datetime(1970, 1, 1, 1, 0)
    dt = dt + timedelta(days=days_delta)
    return dt.astimezone(pytz.timezone(tz))


def get_attr(obj, attr, lang, dt_exec=True):
    request = obj.REQUEST
    request.set('lang', lang)
    if not dt_exec:  # bypass default code execution in ObjAttrs.getObjProperty (Line 579)
        return obj.getObjAttrValue(obj.getObjAttr(attr), REQUEST=request)
    return obj.attr(attr)


def get_attr_by_lang(lang, de, en, fr):

    if lang in ('de', 'ger'):
        return de
    elif lang in ('en', 'eng'):
        return en
    elif lang in ('fr', 'fra'):
        return fr
    else:
        return None


def get_level(obj):
    level = obj.getLevel()
    if level == 0:
        return len(obj.getPath().split('/')) - 2  # calculate for a ZMSSite at content level
    return level


def get_type(obj):
    if '/unibiblio' in obj.getPath():
        return SiteType.Library.value  # TODO: remove workaround to override type=Einrichtung
    elif '/unisport' in obj.getPath():
        return SiteType.Unisport.value  # TODO: remove workaround to override type=Einrichtung
    else:
        return obj.attr("attr_dc_type")  # TODO: handle multilang if needed - for ZMSSite not necessary


def get_parent_home_uuid(obj):
    return parse_uuid(getattr(obj.getHome().aq_parent, "content", obj.getHome().content)._uid)


def get_parent_node_uuid(obj):
    if obj.getLevel() > 0 and 'trashcan' not in obj.getParentNode().getId():
        return parse_uuid(obj.getParentNode()._uid)
    else:
        return parse_uuid(obj._uid)


def get_parent_node_sort_id(obj):
    if obj.getLevel() > 0 and 'trashcan' not in obj.getParentNode().getId():
        return obj.getParentNode().getSortId()
    else:
        return 0


def get_children_count(obj, meta_id=None):
    if meta_id is not None:
        return len(obj.zcatalog_index({'path': obj.getPath(),
                                       'meta_id': meta_id}))
    return len(obj.zcatalog_index({'path': obj.getPath()}))


def parse_uuid(uuid):
    return UUID(f'urn:uuid:{uuid}')


def parse_datetime(value):
    try:
        return pytz.timezone('Europe/Zurich').localize(datetime(*value[:6]))
    except (ValueError, TypeError):
        return datetime(1970, 1, 1)


def is_activated_by_checkbox_and_timeline(obj, lang):
    # ZMSObject.isVisible() traversing object's hierarchy up to root node and checks if
    # - object is translated
    # - object has been committed
    # - object is not in trashcan
    # - object is activated -> ('active' is True) AND ('attr_active_start' < NOW < 'attr_active_end')
    request = obj.REQUEST
    request.set('lang', lang)
    return len(list(filter(lambda x: not x.isVisible(REQUEST=request),
                           obj.breadcrumbs_obj_path(portalMaster=False)))) == 0


def get_url(obj, attr, lang=None, obj_context_href=False):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())

    if obj_context_href:
        return strip_cmstest(obj.getHref2IndexHtmlInContext(context=None, REQUEST=request))

    assert attr is not None, 'attr must not be None'
    value = obj.attr(attr)

    if isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile):
        return get_url_from_conf_or_env(obj) + value.getHref(REQUEST=request)

    if isinstance(value, str) and value.startswith('{$uid:') and value.endswith('}'):
        lang_target = lang
        if ';lang=' in value:
            lang_target = re.sub(r'{\$uid:(.*);lang=(\w*)}', r'\2', value)
        request.set('lang', lang_target)
        return strip_cmstest(obj.getLinkUrl(value, REQUEST=request))
    
    return value


def get_size(obj, attr, lang=None):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())
    value = obj.attr(attr)
    
    if isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile):
        return value.get_size()
    
    return 0


def get_url_from_conf_or_env(obj):
    if obj is None:
        return ''
    prot = obj.getAbsoluteHome().portal.content.getConfProperty('ASP.protocol')
    host = obj.getAbsoluteHome().portal.content.getConfProperty('UniBE.Server')
    # Overwrite by environment variable if set
    # ZMS_URL=http://127.0.0.1:8080 -> e.g. on localhost
    return os.getenv('ZMS_URL', f'{prot}://{strip_cmstest(host)}')


def strip_cmstest(domain):
    if domain is None:
        return ''
    if standard.pybool(os.getenv('STRIP_CMSTEST', True)):
        return domain.replace('cmstest1.', '').replace('cmstest.', '').replace('cms.test.', '').replace('cmsint.', '')
    return domain


def get_data(obj, attr, lang=None):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())

    value = obj.attr(attr)

    # TODO: check if _blobfields.MyImage is a valid use case
    if isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile):
        href = value.getHref(REQUEST=request)
        href = f'{get_url_from_conf_or_env(obj)}{href}'
        try:
            if href.endswith('.json'):
                json = requests.get(url=href, timeout=10).json()
                return str(json)
            else:
                text = requests.get(url=href, timeout=10).text
                return str(text)
        except:
            debug(href)
            return None


# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
