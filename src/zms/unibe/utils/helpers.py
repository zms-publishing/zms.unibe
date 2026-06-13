import logging
import os
import pytz
import re
import requests
import time
import zExceptions

from bs4 import BeautifulSoup
from babel.dates import (format_date, 
                         format_time, 
                         format_datetime, 
                         format_timedelta, 
                         get_timezone, 
                         get_timezone_name)
from datetime import (datetime,
                      timedelta)
from DateTime import DateTime  # legacy Zope implementation, returned e.g. by ZopeTime()
from markitdown import MarkItDown
from markdown import markdown as render_as_html
from io import BytesIO
from uuid import UUID

from AccessControl import ModuleSecurityInfo
from Products.zms import standard, _blobfields

from .enums import SiteType

security = ModuleSecurityInfo('zms.unibe.utils.helpers')  # allow module import in RestrictedPython

LOGGER = logging.getLogger('zms.unibe.utils.helpers')


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
    """
    Convert a datetime, timestamp, or ISO8601 string to the specified local timezone.

    This function takes a datetime object or other datetime representations such 
    as ISO8601 strings, struct_time objects, or UNIX timestamps and converts them 
    to the specified timezone. If no timezone is provided, it defaults to 'Europe/Zurich'. 
    The function optionally adjusts the datetime by a specified number of days before 
    performing the timezone conversion.

    :param dt: The datetime input, which can be a datetime object, ISO8601 string, 
        struct_time object, or a UNIX timestamp (int or float). If no value 
        is provided, the current datetime will be used.
    :type dt: Optional[Union[datetime, str, time.struct_time, int, float, DateTime]]

    :param tz: The timezone to convert the datetime to. If it is not provided, the 
        timezone 'Europe/Zurich' will be used.
    :type tz: Optional[str]

    :param days_delta: Number of days to adjust the datetime before converting it 
        to the specified timezone.
    :type days_delta: int

    :return: A timezone-aware datetime object in the specified timezone.
    :rtype: datetime
    """
    try:
        tz = pytz.timezone(tz)
    except pytz.UnknownTimeZoneError:
        tz = pytz.timezone('Europe/Zurich')
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
    return dt.astimezone(tz)


print('Addon: zms.unibe.utils.helpers.is_authorized')
@security.public
def is_authorized(context, roles, acquired=False, raise_exception=True):
    """
    Helper function to be used in custom Python Scripts or External Methods.
    The execution of such code can thus be limited to users with explicit set
    roles in the given context/client. It can be restricted even for
    ZMSAdministrators and Managers in upper hierarchy levels, e.g., if the
    data is confidential and should not be exposed without explicit permission.

    The user is granted access if they have created the object in the given context.

    Use Case:
     -> assert is_authorized(self, ('ZMSAdministrator', 'ZMSEditor'), acquired=False)
        /manage_survey_data of a specific ZMSSurveyJS should only be
        accessible for users with roles explicitly set in the according client,
        even if they are global ZMSAdministrators or Managers.

    The function determines authorization by comparing the roles assigned to the
    authenticated user in the current context and the roles set within the client's
    object path hierarchy. It may raise an exception if the user is not authorized.

    Args:
        context (object): The context in which the authorization check is performed.
        roles (list of str): List of roles to check against the user's roles.
        acquired (bool, optional): Indicates whether to include roles acquired
            from parent contexts. Defaults to False.
        raise_exception (bool, optional): Determines if an exception should be
            raised when the user is not authorized. Defaults to True.

    Returns:
        bool: True if the user is authorized, otherwise False.

    Raises:
        zExceptions.Unauthorized: If the user is not authorized and
            raise_exception is set to True.
    """
    auth_user = context.REQUEST.get('AUTHENTICATED_USER')

    if context.attr('created_uid') == str(auth_user):
        return True

    try:  # available only in ZMS context
        sec_users = context.getSecurityUsers(acquired=acquired)
        nodes = sec_users.get(str(auth_user), {}).get('nodes', {})
        obj_path_breadcrumbs = context.breadcrumbs_obj_path(portalMaster=acquired)
    except AttributeError:
        nodes = {}
        obj_path_breadcrumbs = []

    # Check if one of the given roles is assigned to the authenticated user
    # and the role is set in the path hierarchy of the current client
    # or in a parent hierarchy if acquired is True.
    obj_path_roles = []
    for obj_path in obj_path_breadcrumbs:
        obj_path_uid = f'{{${obj_path.get_uid()}}}'
        obj_path_roles.extend(nodes.get(obj_path_uid, {}).get('roles', []))

    if isinstance(roles, str):
        roles = (roles,)  # make tuple to avoid search for 'Manager' in string
    has_role_in_obj_path = len([x for x in roles if x in set(obj_path_roles)]) > 0
    has_role_manager = (('Manager' in roles) and
                        ('Manager' in auth_user.getRolesInContext(context)))

    if has_role_in_obj_path or has_role_manager:
        return True
    if raise_exception:
        raise zExceptions.Unauthorized
    return False


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


def parse_datetime(value):
    try:
        return pytz.timezone('Europe/Zurich').localize(datetime(*value[:6]))
    except (ValueError, TypeError):
        return datetime(1970, 1, 1)


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
    try:
        prot = obj.getAbsoluteHome().portal.content.getConfProperty('ASP.protocol')  # https
        host = obj.getAbsoluteHome().portal.content.getConfProperty('UniBE.Server')  # www.unibe.ch
    except AttributeError:
        prot = 'http'
        host = '127.0.0.1:8080'
    # Overwrite by environment variable if set
    return os.getenv('ZMS_URL', f'{prot}://{strip_cmstest(host)}')


def strip_cmstest(domain):
    if domain is None:
        return ''
    if standard.pybool(os.getenv('STRIP_CMSTEST', True)):
        return domain.replace('cmstest1.', '').replace('cmstest.', '').replace('cms.test.', '').replace('cmsint.', '')
    return domain


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

print('Addon: zms.unibe.utils.helpers.get_when')
@security.public
def get_when(dt, mode=None,
             locale='de_CH', tz='Europe/Zurich', 
             granularity='second', threshold=0.85,
             format='long', add_direction=True):
    """
    Determines and returns a formatted representation of the input date, time, or timedelta 
    based on the specified `mode` and formatting criteria. Handles localization, time zone 
    adjustments, and granularity for delta formats.
    
    It is basically a wrapper for https://babel.pocoo.org/en/latest/dates.html

    :param dt: Input date, time, or timedelta. Can be a `datetime`, `date`, or a number 
               (interpreted as days). This parameter determines the entity to be formatted 
               based on the given `mode`.
    :type dt: datetime | date | timedelta | int | float
    :param mode: Specifies the formatting operation to perform. Options include:
                 - 'date': Formats only the date.
                 - 'time': Formats only the time.
                 - 'day': Formats the day of the month.
                 - 'weekday': Formats the name of the weekday.
                 - 'delta': Formats timedelta with varying granularity and threshold.
                 - Other values are interpreted as explicit format strings or defaulted
                   to ISO8601 if not recognized.
    :type mode: str | None
    :param locale: Locale string for localized formatting. Defaults to 'de_CH'.
    :type locale: str
    :param tz: Timezone information for adjusting the datetime. Defaults to 'Europe/Zurich' 
               if the provided timezone is unrecognized or `None`.
    :type tz: str | None
    :param granularity: Defines the smallest time unit (e.g., 'second', 'minute', 'day') 
                        for timedelta formatting when the mode is 'delta'. Defaults to 'second'.
    :type granularity: str
    :param threshold: Threshold value determining when to step into the next higher 
                      granularity for timedelta formatting. Defaults to 0.85.
    :type threshold: float
    :param format: Specifies the verbosity of the output in timedelta formatting (e.g., 'short', 
                   'long'). Defaults to 'long'.
    :type format: str
    :param add_direction: When `True`, includes direction indicators (e.g., 'in', 'ago') 
                          in timedelta formatting. Defaults to `True`.
    :type add_direction: bool
    :return: Returns a string representing the formatted input based on the specified mode 
             and locale. The format varies depending on the mode. Examples include formatted 
             dates, times, weekdays, and timedelta durations.
    :rtype: str
    """
    try:
        tz = get_timezone(tz)
    except LookupError:
        tz = get_timezone('Europe/Zurich')
    tzname = get_timezone_name(tz, return_zone=True)
    
    if isinstance(dt, timedelta):
        mode = 'delta'
    
    match mode:
        case 'date':
            return format_date(local_timezone(dt, tz=tzname),
                               format='long',
                               locale=locale)
        case 'time':
            return format_time(local_timezone(dt, tz=tzname),
                               format='short',
                               locale='de',  # enforce 24h format to avoid AM/PM
                               tzinfo=tz)
        case 'day':
            return format_date(local_timezone(dt, tz=tzname),
                               format='d',
                               locale=locale)
        case 'weekday':
            return format_date(local_timezone(dt, tz=tzname),
                               format='E',
                               locale=locale).replace('.', '')
        case 'delta':
            if not isinstance(dt, timedelta):
                try:
                    dt = timedelta(days=dt)
                except TypeError:
                    dt = timedelta(days=0)
            # https://babel.pocoo.org/en/latest/dates.html#time-delta-formatting
            return format_timedelta(dt,
                                    locale=locale,
                                    granularity=granularity,
                                    threshold=threshold,
                                    format=format,
                                    add_direction=add_direction)
        case x if x not in (
            None, 'iso', 'iso8601'):
            # https://babel.pocoo.org/en/latest/dates.html#pattern-syntax
            return format_datetime(local_timezone(dt, tz=tzname),
                                   format=mode,
                                   locale=locale,
                                   tzinfo=tz)
    # return ISO8601 format as default
    return format_datetime(local_timezone(dt, tz=tzname),
                           format="yyyy-MM-dd'T'HH:mm:ssZZZZZ",
                           tzinfo=tz)


print('Addon: zms.unibe.utils.helpers.sanitize_html')
@security.public
def sanitize_html(content, return_type='html'):
    """
    Sanitizes HTML content by converting it into either plain markdown or sanitized HTML.
    If the content starts with <html>, it uses the MarkItDown library to sanitize and
    convert it to markdown. Alternatively, the markdown is converted back to HTML,
    performing additional cleaning such as removing images, empty paragraphs, and
    unwanted newline characters.

    If errors occur, it uses BeautifulSoup to extract text content.

    Parameters:
    content (str): The input HTML content to be sanitized or processed.

    return_type (str, optional): Specifies the type of value to return:
        - 'markdown': Converts the HTML to Markdown and returns it.
        - 'html': Sanitizes the HTML, removing unwanted elements, and returns cleaned HTML.
        - 'href': Extracts and returns the last hyperlink ('<a href="...">') present in the HTML.
        Default is 'html'.

    Returns:
    str: The output in the format specified by `return_type`.

    Raises:
    Does not explicitly raise errors but logs any exceptions that occur during processing.
    """
    try:
        if content.startswith('<html>') and return_type in ('markdown', 'html'):
            md = MarkItDown()
            stream = BytesIO(content.encode(encoding="utf-8"))
            markdown = md.convert_stream(stream).text_content
            markdown = markdown.replace('\xa0', ' ')  # non-breaking space in Latin1 (ISO 8859-1)
            if return_type == 'markdown':
                return markdown
            elif return_type == 'html':
                html = render_as_html(markdown)
                html = re.compile(r'<img.*?/>').sub('', html)
                html = html.replace('<p></p>', '')
                html = html.replace('\n', ' ')
                return html.strip()

    except Exception as e:
        LOGGER.error(f'Error on sanitize_html: {e}')

    soup = BeautifulSoup(content, "html.parser")

    if return_type == 'href':
        links = soup.find_all('a')
        if len(links) > 0:
            # last hyperlink in given HTML
            return links[-1].get('href')

    # extract at least plain text if conversion to markdown or html failed above
    text = soup.get_text()
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', '')
    text = text.replace('  ', ' ')
    return text.strip()


# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
