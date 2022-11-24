import glob
import importlib.util
import inspect
import pytz
import sys
import os
import xmltodict
from enum import Enum
from datetime import datetime
from Products.zms import _blobfields

PATH = os.path.abspath(os.path.dirname(__file__))
PATH = PATH.startswith('/app') and PATH + '/..' or PATH + '/../../unibe-cms'

ZMS_METAS_PATH = f'{PATH}/frontend/ZMSModels/*/*/metaobj_manager/__metas__.py'
ZMS_MODEL_PATH = f'{PATH}/frontend/ZMSModels/*/*/metaobj_manager/*/*/__init__.py'
ZMS_METAS_ATTR = {}
ZMS_MODEL_ATTR = {}


class Lang(str, Enum):
    de = 'de'
    en = 'en'
    fr = 'fr'


class SiteType(str, Enum):
    Abteilung = "Abteilung"
    Bereich = "Bereich"
    Department = "Department"
    Einrichtung = "Einrichtung"
    Fakultaet = "Fakultaet"
    Home = "Home"
    Institut = "Institut"
    Microsite = "Microsite"
    Uniaktuell = "Uniaktuell"


class AttrType(str, Enum):
    all = "*"
    amount = "amount"
    boolean = "boolean"
    date = "date"
    datetime = "datetime"
    file = "file"
    identifier = "identifier"
    image = "image"
    list = "list"
    multiselect = "multiselect"
    password = "password"
    richttext = "richtext"
    select = "select"
    string = "string"
    text = "text"
    time = "time"
    url = "url"


class MetaObj(str, Enum):
    alertbox = "alertbox"
    bildkachel = "bildkachel"
    carousel = "carousel"
    codeblock = "codeblock"
    contactbox = "contactbox"
    contactboxsection = "contactboxsection"
    contentpane = "contentpane"
    contenttabs = "contenttabs"
    filecontainer = "filecontainer"
    gallery = "gallery"
    hero_2022 = "hero_2022"
    index_a_z = "index_a_z"
    infobox = "infobox"
    linkcontainer = "linkcontainer"
    linkelement = "linkelement"
    media_news = "media_news"
    medienuebersicht = "medienuebersicht"
    navlist = "navlist"
    newsbox = "newsbox"
    newscontainer = "newscontainer"
    person = "person"
    references = "references"
    siteObjMap = "siteObjMap"
    slide = "slide"
    socialmedia_block = "socialmedia_block"
    team = "team"
    teamsection = "teamsection"
    teaser_container_2022 = "teaser_container_2022"
    teaser_element_2022 = "teaser_element_2022"
    twocols = "twocols"
    uniaktuell_index = "uniaktuell_index"
    uniaktuell_search = "uniaktuell_search"
    uniaktuell_uebersicht = "uniaktuell_uebersicht"
    UniaktuellArticle = "UniaktuellArticle"
    UniBEEvent = "UniBEEvent"
    UniBEFactsheet = "UniBEFactsheet"
    video = "video"
    weiterbildung_studiengang = "weiterbildung_studiengang"
    ZMS = "ZMS"
    ZMSAnalytics = "ZMSAnalytics"
    ZMSDataTable = "ZMSDataTable"
    ZMSDocument = "ZMSDocument"
    ZMSFile = "ZMSFile"
    ZMSFolder = "ZMSFolder"
    ZMSFormulator = "ZMSFormulator"
    ZMSFormulatorItem = "ZMSFormulatorItem"
    ZMSGraphic = "ZMSGraphic"
    ZMSLinkContainer = "ZMSLinkContainer"
    ZMSLinkElement = "ZMSLinkElement"
    ZMSNote = "ZMSNote"
    ZMSScheduler = "ZMSScheduler"
    ZMSSchedulerBroker = "ZMSSchedulerBroker"
    ZMSSqlDb = "ZMSSqlDb"
    ZMSSysFolder = "ZMSSysFolder"
    ZMSTable = "ZMSTable"
    ZMSTeaserContainer = "ZMSTeaserContainer"
    ZMSTeaserElement = "ZMSTeaserElement"
    ZMSTextarea = "ZMSTextarea"


def get_zms_model(name=None, types=('*',), metas=True):

    global ZMS_METAS_ATTR
    global ZMS_MODEL_ATTR

    ZMS_MODEL_ATTR = {}
    if metas:
        for module_path in glob.glob(ZMS_METAS_PATH):
            module_name = module_path.rsplit('/', 2)[1]
            _inspect_module(module_name, module_path, types)

    ZMS_METAS_ATTR = ZMS_MODEL_ATTR

    ZMS_MODEL_ATTR = {}
    if name is not None:
        for module_path in glob.glob(ZMS_MODEL_PATH):
            module_name = module_path.rsplit('/', 2)[1]
            if name == module_name:
                _inspect_module(module_name, module_path, types)
                break

    for x in ZMS_MODEL_ATTR:
        if x in ZMS_METAS_ATTR:
            ZMS_MODEL_ATTR[x] = ZMS_METAS_ATTR[x]

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
                    if attr['type'] in ZMS_METAS_ATTR or attr['type'] in types or '*' in types:
                        ZMS_MODEL_ATTR[attr["id"]] = attr


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
    return domain.replace('cmstest1.', '').replace('cmstest.', '').replace('cms.test.', '')


def get_datetime_props(cls):
    props = []
    for key, val in cls.schema()['properties'].items():
        if 'format' in val and val['format'] in ('date', 'date-time'):
            props.append(key)
    return props


def get_attr_value(sql_attr, zms_attr, obj, cls):

    if sql_attr.endswith('_de') and zms_attr.endswith('_ger'):
        lang = 'ger'
        zms_attr = zms_attr[:-4]
    elif sql_attr.endswith('_en') and zms_attr.endswith('_eng'):
        lang = 'eng'
        zms_attr = zms_attr[:-4]
    elif sql_attr.endswith('_fr') and zms_attr.endswith('_fra'):
        lang = 'fra'
        zms_attr = zms_attr[:-4]
    else:
        lang = 'ger'

    if zms_attr == 'obj._uid':
        return obj._uid

    if zms_attr == 'obj.getDocumentElement()._uid':
        return obj.getDocumentElement()._uid

    if zms_attr == 'obj.getParentNode()._uid':
        if obj.getLevel() > 0:
            return obj.getParentNode()._uid
        else:
            return obj._uid

    if zms_attr == 'obj.getHref2IndexHtmlInContext()':
        if sql_attr.endswith('_de'):
            lang = 'ger'
        if sql_attr.endswith('_en'):
            lang = 'eng'
        if sql_attr.endswith('_fr'):
            lang = 'fra'
        return strip_cmstest(
            obj.getHref2IndexHtmlInContext(None, REQUEST={'lang': lang, 'ZMS_CONTEXT_URL': True}))

    if zms_attr == 'obj.getParentNode().attr("title")':
        if sql_attr.endswith('_de'):
            lang = 'ger'
        if sql_attr.endswith('_en'):
            lang = 'eng'
        if sql_attr.endswith('_fr'):
            lang = 'fra'
        if obj.getLevel() > 0:
            return obj.getParentNode().attr("title", REQUEST={'lang': lang})
        else:
            return obj.attr("title", REQUEST={'lang': lang})

    if zms_attr == 'obj.meta_id':
        return obj.meta_id

    if zms_attr == "obj.getLevel()":
        return obj.getLevel()

    if zms_attr == "obj.getPath()":
        return obj.getPath()

    if zms_attr == "obj.getConfProperty('UniBE.Server')":
        return obj.getConfProperty('UniBE.Server')

    if zms_attr == "obj.getConfProperty('UniBE.Alias')":
        return obj.getConfProperty('UniBE.Alias')

    value = obj.attr(zms_attr, REQUEST={'lang': lang})

    if value is not None and (isinstance(value, _blobfields.MyImage) or isinstance(value, _blobfields.MyFile)):
        value = 'https://www.unibe.ch' + value.getHref(REQUEST={'lang': lang})

    if value is not None and isinstance(value, str) and value.startswith('{$uid:'):
        value = strip_cmstest(
            obj.getLinkObj(value).getHref2IndexHtmlInContext(None, REQUEST={'lang': lang, 'ZMS_CONTEXT_URL': True}))

    if zms_attr == 'active':
        value = value and obj.isTranslated(REQUEST={'lang': lang}, lang=lang)
        value = value and len(list(filter(lambda x: not x.isActive(REQUEST={'lang': lang}),
                                          obj.breadcrumbs_obj_path(portalMaster=False)))) == 0

    if sql_attr in get_datetime_props(cls):
        value = value is not None and pytz.timezone('Europe/Zurich').localize(datetime(*value[:6]))

    return value


def local_timezone(dt):
    return dt.astimezone(pytz.timezone('Europe/Zurich'))


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
    uniaktuell_langdict = xmltodict.parse(open(f'{Path(__file__).parent.absolute()}/models/uniaktuell.langdict.xml').read())

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
