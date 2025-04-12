import glob
import importlib.util
import inspect
import pytz
import sys
import os
import io
import re
import xmltodict
import time

from anytree import Node, RenderTree
from anytree.exporter import JsonExporter, DictExporter
from ics import Calendar, Event
from devtools import debug
from uuid import UUID
from enum import Enum
from datetime import datetime
from Products.zms import _blobfields
from zope.globalrequest import setRequest

PATH = os.path.abspath(os.path.dirname(__file__))
PATH = PATH.startswith('/app') and PATH + '/..' or PATH + '/../../..'

ZMS_METAS_PATH = f'{PATH}/frontend/zms/models/*/*/metaobj_manager/__metas__.py'
ZMS_MODEL_PATH = f'{PATH}/frontend/zms/models/*/*/metaobj_manager/*/*/__init__.py'
ZMS_METAS_ATTR = {}
ZMS_MODEL_ATTR = {}

def create_headless_http_request():
    """
    Returns a ZPublisher.HTTPRequest object to be used in headless mode.
    """
    # Measure time for exection.
    import logging
    LOGGER = logging.getLogger('create_headless_http_request')
    start_time = time.time()
    # Imports.  
    from io import BytesIO
    from ZPublisher.HTTPRequest import HTTPRequest
    from ZPublisher.HTTPResponse import HTTPResponse

    env = {}
    env.setdefault('SERVER_NAME', 'nohost')
    env.setdefault('SERVER_PORT', '80')
    resp = HTTPResponse(stdout=BytesIO)

    # Print execution time.
    LOGGER.log(logging.INFO, 'Execution time create_headless_http_request(): %s' % (time.time() - start_time))

    return HTTPRequest(stdin=BytesIO, environ=env, response=resp)

headless_http_request = create_headless_http_request()
# Set defaults
headless_http_request.set('ZMS_CONTEXT_URL', True)
# Set headless_http_request via zope.globalrequest.setRequest.
# The ZMS uses the zope.globalrequest.getRequest as a fallback.
setRequest(headless_http_request)


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
        return 'https://www.unibe.ch' + value.getHref(REQUEST=headless_http_request)
    
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

    if zms_attr == 'obj._uid':
        return obj._uid

    if zms_attr == 'obj._datafilecached':
        return obj.attr('_datafilecached').getData()

    if zms_attr == 'obj.getDocumentElement()._uid':
        return obj.getDocumentElement()._uid

    if zms_attr == 'obj.getParentNode()._uid':
        if obj.getLevel() > 0 and 'trashcan' not in obj.getParentNode().getId():
            return obj.getParentNode()._uid
        else:
            return obj._uid

    if zms_attr == 'obj.getParentHome()._uid':
        return getattr(obj.getHome().aq_parent, 'content', obj.getHome().content)._uid

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
            return len(obj.getPath().split('/'))-2  # calculate for a ZMSSite at content level
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
            return 'Library'  # overwrite deprecated type "Uniaktuell" of UB (Library)
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


def get_sections_tree(data, lang):

    root = Node(str(UUID('2780d477-f517-49bb-a0f4-c46b56eeaab2')),
                title='UniBE')
    nodes = {}

    # set nodes with parent == root
    for i, obj in enumerate(data):
        if obj.parent_uuid == UUID('2780d477-f517-49bb-a0f4-c46b56eeaab2') and \
                obj.uuid != UUID('2780d477-f517-49bb-a0f4-c46b56eeaab2'):
            nodes[obj.uuid] = Node(str(obj.uuid), parent=root,
                                   domain=strip_cmstest(obj.domain),
                                   title=get_attr_by_lang(lang,
                                                          de=obj.title_de,
                                                          en=obj.title_en,
                                                          fr=obj.title_fr),
                                   type=obj.type,
                                   path=obj.path,  # Beware: 'path' is a reserved attribute of anytree
                                   uuid=obj.uuid)

    # set nodes with parent != root
    for i, obj in enumerate(data):
        if obj.parent_uuid != UUID('2780d477-f517-49bb-a0f4-c46b56eeaab2') and \
                obj.uuid != UUID('2780d477-f517-49bb-a0f4-c46b56eeaab2'):
            nodes[obj.uuid] = Node(str(obj.uuid),
                                   domain=strip_cmstest(obj.domain),
                                   title=get_attr_by_lang(lang,
                                                          de=obj.title_de,
                                                          en=obj.title_en,
                                                          fr=obj.title_fr),
                                   type=obj.type,
                                   path=obj.path,  # Beware: 'path' is a reserved attribute of anytree
                                   uuid=obj.uuid)

    # set parent nodes - prerequiste: order_by(model.ZMSSite.level) to process in hierachy
    for i, obj in enumerate(data):
        if obj.parent_uuid in nodes.keys():
            nodes[obj.uuid] = Node(str(obj.uuid), parent=nodes[obj.parent_uuid],
                                   domain=strip_cmstest(obj.domain),
                                   title=get_attr_by_lang(lang,
                                                          de=obj.title_de,
                                                          en=obj.title_en,
                                                          fr=obj.title_fr),
                                   type=obj.type,
                                   path=obj.path,  # Beware: 'path' is a reserved attribute of anytree
                                   uuid=obj.uuid)
        elif obj.parent_uuid != UUID('2780d477-f517-49bb-a0f4-c46b56eeaab2'):
            debug(obj.parent_uuid)

    for pre, fill, node in RenderTree(root):
        # print("%s%s" % (pre, node.title))
        pass

    jsonexporter = JsonExporter(indent=2, sort_keys=True, ensure_ascii=False)
    # print(jsonexporter.export(root))

    dictexporter = DictExporter(attriter=lambda attrs: [(k, v) for k, v in attrs if k != "name"])

    return dictexporter.export(root)


def generate_ics(lang, results):

    calendar = Calendar()

    for res in results:
        event = Event()
        event.name = get_attr_by_lang(lang,
                                      de=res.NewsEvents.title_de,
                                      en=res.NewsEvents.title_en,
                                      fr=res.NewsEvents.title_fr)
        event.begin = local_timezone(res.NewsEvents.start_dt)
        event.end = local_timezone(res.NewsEvents.end_dt)
        event.description = get_attr_by_lang(lang,
                                             de=res.NewsEvents.infos_de,
                                             en=res.NewsEvents.infos_en,
                                             fr=res.NewsEvents.infos_fr)
        event.location = get_attr_by_lang(lang,
                                          de=res.NewsEvents.location_de,
                                          en=res.NewsEvents.location_en,
                                          fr=res.NewsEvents.location_fr)
        event.url = get_attr_by_lang(lang,
                                     de=res.NewsEvents.url_de,
                                     en=res.NewsEvents.url_en,
                                     fr=res.NewsEvents.url_fr)
        calendar.events.add(event)

    return io.StringIO(calendar.serialize())
