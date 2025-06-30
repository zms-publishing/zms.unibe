import os
import re
from datetime import datetime
from enum import Enum
from uuid import UUID

import pytz
import requests
import xmltodict
from Products.zms import _blobfields
from devtools import debug

from ..headless import headless_http_request


class Lang(str, Enum):
    de = 'de'
    en = 'en'
    fr = 'fr'


class SiteType(str, Enum):
    Fakultaet = "Fakultaet"
    Departement = "Departement"
    Institut = "Institut"
    Abteilung = "Abteilung"
    Bereich = "Bereich"
    Einrichtung = "Einrichtung"
    Microsite = "Microsite"
    Library = "Library"
    Unisport = "Unisport"


def get_attr_by_lang(lang, de, en, fr):

    if lang == 'de':
        return de
    elif lang == 'en':
        return en
    elif lang == 'fr':
        return fr
    else:
        return None


def get_uniaktuell_lang_str(lang, key):

    from pathlib import Path
    uniaktuell_langdict = xmltodict.parse(open(f'{Path(__file__).parent.absolute()}/uniaktuell.langdict.xml').read())

    if lang == 'de':
        lang = 'ger'
    elif lang == 'en':
        lang = 'eng'
    elif lang == 'fr':
        lang = 'fra'

    for i in uniaktuell_langdict['list']['item']:
        for j in i['dictionary']['item']:
            if '#text' in j:
                if j['#text'] == key:
                    for x in i['dictionary']['item']:
                        if '#text' in x and x['@key'] == lang:
                            return x['#text']
    return ''


def get_subdomain(domain, reverse=False):
    if domain is None:
        return ''
    if reverse:
        rtn = domain == 'portal' and 'www.cmstest1.unibe.ch' or f'www.{domain}.cmstest1.unibe.ch'
        rtn = domain == 'intern' and 'intern.cmstest1.unibe.ch' or rtn
        rtn = domain == 'sam.intern' and 'sam.intern.cmstest1.unibe.ch' or rtn
        return rtn
    rtn = domain.replace('cmstest1.', '').replace('www.unibe.ch', 'portal')
    return rtn.replace('www.', '').replace('.unibe.ch', '')


def strip_cmstest(domain):
    if domain is None:
        return ''
    return domain.replace('cmstest1.', '').replace('cmstest.', '').replace('cms.test.', '').replace('cmsint.', '')


def get_url_from_conf_or_env(obj):
    if obj is None:
        return ''
    prot = obj.getAbsoluteHome().portal.content.getConfProperty('ASP.protocol')
    host = obj.getAbsoluteHome().portal.content.getConfProperty('UniBE.Server')
    # Overwrite by environment variable if set
    # ZMS_URL=http://127.0.0.1:8080 -> e.g. on localhost
    return os.getenv('ZMS_URL', f'{prot}://{strip_cmstest(host)}')


def get_datetime_props(cls):
    props = []
    for key, val in cls.schema()['properties'].items():
        if 'anyOf' in val:
            if ('format' in val['anyOf'][0] and val['anyOf'][0]['format'] 
                in ('date', 'date-time')):
                props.append(key)
    return props


def get_attr_value(sql_attr, zms_attr, obj, cls):
    if zms_attr[-4:] in ('_ger', '_eng', '_fra'):
        zms_attr = zms_attr[:-4]

    if sql_attr.endswith('_de'):
        lang = 'ger'
    elif sql_attr.endswith('_en'):
        lang = 'eng'
    elif sql_attr.endswith('_fr'):
        lang = 'fra'
    else:
        lang = 'ger'

    headless_http_request.set('lang', lang)

    value = obj.attr(zms_attr, REQUEST=headless_http_request)

    if sql_attr in get_datetime_props(cls):
        try:
            return pytz.timezone('Europe/Zurich').localize(datetime(*value[:6]))
        except (ValueError, TypeError):
            return datetime(1970, 1, 1)

    if isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile):
        if '_size' in sql_attr:
            return value.get_size()
        return get_url_from_conf_or_env(obj) + value.getHref(REQUEST=headless_http_request)

    if isinstance(value, str) and value.startswith('{$uid:'):
        lang_target = lang
        if ';lang=' in value:
            lang_target = re.sub(r'{\$uid:(.*);lang=(\w*)}', r'\2', value)
        headless_http_request.set('lang', lang_target)
        return strip_cmstest(obj.getLinkObj(value).getHref2IndexHtmlInContext(None, REQUEST=headless_http_request))

    # extract parameter between parenthesis in zms_attr
    param = None
    regex = re.search(pattern=r'\((.+)\)', string=zms_attr)
    if regex is not None:
        res = regex.groups()
        if type(res) is tuple and len(res) > 0:
            param = res[0]
            if param[-4:] in ('_ger', '_eng', '_fra'):
                param = param[:-4]

    if 'obj.getObjChildren' in zms_attr:
        if param is not None:
            return len(obj.getObjChildren(id=param, REQUEST=headless_http_request))
        else:
            return 0

    if 'obj.getObjAttrValue' in zms_attr:
        if param is not None:
            attr = obj.getObjAttr(param)
            return obj.getObjAttrValue(attr, REQUEST=headless_http_request)
        else:
            return ''

    if 'obj.getConfProperty' in zms_attr:
        if param is not None:
            return obj.getConfProperty(key=param)
        else:
            return ''

    if 'obj.getData' in zms_attr:
        if param is not None:
            value = obj.attr(param, REQUEST=headless_http_request)
            if isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile):
                href = obj.attr(param, REQUEST=headless_http_request).getHref(REQUEST=headless_http_request)
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
        return None

    if zms_attr == 'obj._uid':
        return UUID(f'urn:uuid:{obj._uid}')

    if zms_attr == 'obj.getDocumentElement()._uid':
        return UUID(f'urn:uuid:{obj.getDocumentElement()._uid}')

    if zms_attr == 'obj.getParentNode()._uid':
        if obj.getLevel() > 0 and 'trashcan' not in obj.getParentNode().getId():
            return UUID(f'urn:uuid:{obj.getParentNode()._uid}')
        else:
            return UUID(f'urn:uuid:{obj._uid}')

    if zms_attr == 'obj.getParentHome()._uid':
        return UUID(f'urn:uuid:{getattr(obj.getHome().aq_parent, "content", obj.getHome().content)._uid}')

    if zms_attr == 'obj.getHref2IndexHtmlInContext()':
        return strip_cmstest(
            obj.getHref2IndexHtmlInContext(None, REQUEST=headless_http_request))

    if zms_attr == 'obj.getParentNode().title':
        if obj.getLevel() > 0 and 'trashcan' not in obj.getParentNode().getId():
            return obj.getParentNode().attr("title", REQUEST=headless_http_request)
        else:
            return obj.attr("title", REQUEST=headless_http_request)

    if zms_attr == 'obj.meta_id':
        return obj.meta_id

    if zms_attr == "obj.getLevel()":
        level = obj.getLevel()
        if level == 0:
            return len(obj.getPath().split('/')) - 2  # calculate for a ZMSSite at content level
        return level

    if zms_attr == "obj.getSortId()":
        return obj.getSortId()

    if zms_attr == "obj.getParentNode().getSortId()":
        if obj.getLevel() > 0 and 'trashcan' not in obj.getParentNode().getId():
            return obj.getParentNode().getSortId()
        else:
            return 0

    if zms_attr == "obj.getPath()":
        return obj.getPath()

    if zms_attr == "obj.getCount()":
        # handled for ZMSSite.count_objs in commands.update_tables()
        return

    if zms_attr == "obj.getType()":
        if '/unibiblio' in obj.getPath():
            return SiteType.Library.value  # TODO: remove workaround to override type=Einrichtung
        elif '/unisport' in obj.getPath():
            return SiteType.Unisport.value  # TODO: remove workaround to override type=Einrichtung
        else:
            return obj.attr("attr_dc_type")  # TODO: handle multilang if needed - for ZMSSite not necessary

    if zms_attr == 'obj.isActivatedByCheckboxAndTimeline()':
        # ZMSObject.isVisible() traversing object's hierarchy up to root node and checks if
        # - object is translated
        # - object has been committed
        # - object is not in trashcan
        # - object is activated -> ('active' is True) AND ('attr_active_start' < NOW < 'attr_active_end')
        return len(list(filter(lambda x: not x.isVisible(REQUEST=headless_http_request),
                               obj.breadcrumbs_obj_path(portalMaster=False)))) == 0

    return value
