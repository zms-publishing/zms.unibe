import logging
import os
import re
from uuid import UUID

import requests

try:
    from Products.zms import _blobfields, standard
except ImportError:
    pass  # ZMS-dependent getters require the optional zope extra.
from ..enums import SiteType

LOGGER = logging.getLogger('zms.unibe.utils.zms2sql.getters')


def strip_cmstest(domain):
    if domain is None:
        return ''
    if standard.pybool(os.getenv('STRIP_CMSTEST', True)):
        return domain.replace('cmstest1.', '').replace('cmstest.', '').replace('cms.test.', '').replace('cmsint.', '')
    return domain


def get_attr(obj, attr, lang=None, dt_exec=True):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())
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
    if obj.getLevel() > 0 and '/trashcan' not in obj.getPath():
        return parse_uuid(obj.getParentNode()._uid)
    else:
        return parse_uuid(obj._uid)


def get_parent_node_sort_id(obj):
    if obj.getLevel() > 0 and '/trashcan' not in obj.getPath():
        return obj.getParentNode().getSortId()
    else:
        return 0


def get_parent_node_attr(obj, attr, lang=None, dt_exec=True):
    lang = lang or obj.getPrimaryLanguage()
    if obj.getLevel() > 0 and '/trashcan' not in obj.getPath():
        return get_attr(obj.getParentNode(), attr, lang, dt_exec)
    else:
        return get_attr(obj, attr, lang, dt_exec)


def get_children_count(obj, meta_id=None):
    if meta_id is not None:
        return len(obj.zcatalog_index({'path': obj.getPath(),
                                       'meta_id': meta_id}))
    return len(obj.zcatalog_index({'path': obj.getPath()}))


def parse_uuid(uuid):
    return UUID(f'urn:uuid:{uuid.replace("uid:", "")}')


def is_activated_by_checkbox_and_timeline(obj, lang=None):
    # ZMSObject.isVisible() traversing object's hierarchy up to root node and checks if
    # - object is translated
    # - object has been committed
    # - object is not in trashcan
    # - object is activated -> ('active' is True) AND ('attr_active_start' < NOW < 'attr_active_end')
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())
    return len(list(filter(lambda x: not x.isVisible(REQUEST=request),
                           obj.breadcrumbs_obj_path(portalMaster=False)))) == 0


def get_url(obj, attr, lang=None):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())

    if attr is None:  # return obj's url with subdomain from config-properties
        return strip_cmstest(obj.getHref2IndexHtmlInContext(context=None, REQUEST=request))

    value = obj.attr(attr)

    if isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile):
        return strip_cmstest(get_url_from_conf_or_env(obj)) + value.getHref(REQUEST=request)

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
    try:
        prot = obj.getAbsoluteHome().portal.content.getConfProperty('ASP.protocol')  # https
        host = obj.getAbsoluteHome().portal.content.getConfProperty('UniBE.Server')  # www.unibe.ch
    except AttributeError:
        prot = 'http'
        host = '127.0.0.1:8080'
    # Overwrite by environment variable if set
    return os.getenv('ZMS_URL', f'{prot}://{host}')


def get_data(obj, attr, lang=None, json_as_py=False):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())

    value = obj.attr(attr)

    if isinstance(value, _blobfields.MyFile) or isinstance(value, _blobfields.MyImage):
        href = value.getHref(REQUEST=request)
        href = f'{get_url_from_conf_or_env(obj)}{href}'
        response = requests.get(url=href, timeout=10)

        if response.status_code == 200:
            if response.apparent_encoding in ('ascii', 'utf-8'):
                if href.endswith('.json') and json_as_py:
                    return response.json(), response.headers
                else:
                    return response.text, response.headers
            else:
                return response.content, response.headers
        else:
            LOGGER.error(f'Error on get_data: {response.status_code} {href}')

    return None, None


def get_json_schema(obj, lang=None):
    request = obj.REQUEST
    request.set('lang', lang or obj.getPrimaryLanguage())

    href = f'{get_url_from_conf_or_env(obj)}{obj.getPath()}/getJSONSchema'
    response = requests.get(url=href, timeout=10)

    if response.status_code == 200:
        return response.text
    else:
        LOGGER.error(f'Error on get_json_schema: {response.status_code} {href}')
    return None
