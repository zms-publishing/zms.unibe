import logging
import time as t
from datetime import date, datetime, time, timedelta
from typing import Any
from unittest.mock import MagicMock

import pytz  # TODO: replace by zoneinfo
from DateTime import DateTime  # legacy Zope implementation, returned e.g. by ZopeTime()
from babel.dates import format_date, format_datetime, format_time, format_timedelta
from babel.dates import get_timezone, get_timezone_name

from .MockDecorator import MockDecorator

try:
    import zExceptions
    from AccessControl import ModuleSecurityInfo

    security = ModuleSecurityInfo('zms.unibe.helpers.datetime')  # allow module import in RestrictedPython
except:
    security = MagicMock()  # fallback if no Zope/ZMS context available
    security.public = MagicMock(wraps=MockDecorator())

LOGGER = logging.getLogger('zms.unibe.helpers.datetime')


print('Helper: zms.unibe.helpers.datetime.local_timezone')
@security.public
def local_timezone(dt: Any = None,
                   tz: str = 'Europe/Zurich',
                   days_delta: int = 0) -> datetime:
    """
    Convert a datetime, timestamp, or ISO8601 string to the specified local timezone.

    This function takes a datetime object or other datetime representations such 
    as ISO8601 strings, struct_time objects, or UNIX timestamps and converts them 
    to the specified timezone. If no timezone is provided, it defaults to 'Europe/Zurich'. 
    The function optionally adjusts the datetime by a specified number of days before 
    performing the timezone conversion.

    :param dt: The datetime input, which can be a datetime or date object, ISO8601 string, 
        struct_time object, or a UNIX timestamp (int or float). If no value 
        is provided, the current datetime will be used.
    :type dt: Optional[Union[datetime, date, str, time.struct_time, int, float, DateTime]]

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
    try:
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        elif isinstance(dt, int) or isinstance(dt, float):
            dt = datetime.fromtimestamp(dt)
    except (ValueError, TypeError):
        dt = datetime.fromtimestamp(0)  # datetime.datetime(1970, 1, 1, 1, 0)
    if dt is None:
        dt = datetime.now()
    elif isinstance(dt, t.struct_time):
        dt = datetime.fromtimestamp(t.mktime(dt))
    elif isinstance(dt, DateTime):  # legacy Zope implementation, returned e.g. by ZopeTime()
        dt = datetime.fromisoformat(dt.ISO8601())
    elif type(dt) is date:
        # Please note: isinstance(dt, date) is also True for datetime objects, because datetime is a subclass of date
        # add 00:00:00 to a plain date object so that the time zone can be set to the datetime object in the next step
        dt = datetime.combine(dt, datetime.min.time())
    elif type(dt) is time:
        dt = datetime.combine(datetime.now().date(), dt)
    dt = dt + timedelta(days=days_delta)
    return dt.astimezone(tz)


print('Helper: zms.unibe.helpers.datetime.get_when')
@security.public
def get_when(dt: Any = None,
             mode: str | None = None,
             locale: str = 'de_CH',
             tz: str = 'Europe/Zurich',
             granularity: str = 'second',
             threshold: float | int = 0.85,
             format: str = 'long',
             add_direction: bool = True) -> str:
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
                           locale=locale,
                           tzinfo=tz)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
