# Refactored by GitHub Copilot ChatGPT-6 Luna 

import logging
import time as t
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from typing import Any
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from DateTime import DateTime  # legacy Zope implementation, returned e.g. by ZopeTime()
from babel.dates import format_date, format_datetime, format_time, format_timedelta

from .MockDecorator import MockDecorator

try:
    import zExceptions
    from AccessControl import ModuleSecurityInfo

    security = ModuleSecurityInfo('zms.unibe.helpers.datetime')  # allow module import in RestrictedPython
except:
    security = MagicMock()  # fallback if no Zope/ZMS context available
    security.public = MagicMock(wraps=MockDecorator())

LOGGER = logging.getLogger('zms.unibe.helpers.datetime')


DEFAULT_TIMEZONE = 'Europe/Zurich'
_DATETIME_TYPE = datetime


def _resolve_timezone(tz: str | tzinfo | None) -> tzinfo:
    if tz is None:
        return ZoneInfo(DEFAULT_TIMEZONE)
    if isinstance(tz, str):
        try:
            return ZoneInfo(tz)
        except (ZoneInfoNotFoundError, ValueError):
            return ZoneInfo(DEFAULT_TIMEZONE)
    return tz


def _attach_timezone(dt: datetime, tz: tzinfo) -> datetime:
    if dt.tzinfo is not None:
        return dt
    return dt.replace(tzinfo=tz)


print('Helper: zms.unibe.helpers.datetime.local_timezone')
@security.public
def local_timezone(dt: Any = None,
                   tz: str | tzinfo | None = None,
                   days_delta: int = 0) -> datetime:
    """
    Convert a date/time value to a timezone-aware datetime.

    Naive calendar values are interpreted as wall times in the target timezone.
    Aware values are converted without changing their represented instant. An
    aware ISO8601 string retains its offset when no timezone is explicitly given.
    Unix timestamps represent instants; ``struct_time`` is interpreted in the
    system timezone. Invalid ISO8601 strings fall back to the Unix epoch.

    :param dt: A datetime, date, time, ISO8601 string, ``struct_time``,
        Unix timestamp, legacy Zope ``DateTime``, or ``None`` for the current time.
    :param tz: Target IANA timezone name or tzinfo object. Defaults to
        ``Europe/Zurich``; an aware ISO8601 string supplies its timezone if omitted.
    :param days_delta: Number of days to add before converting to the target timezone.
    :return: A timezone-aware datetime in the resolved timezone.
    """
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            dt = datetime.fromtimestamp(0, tz=timezone.utc)
        else:
            if tz is None and dt.tzinfo is not None:
                tz = dt.tzinfo
    elif isinstance(dt, (int, float)):
        dt = datetime.fromtimestamp(dt, tz=timezone.utc)

    target_timezone = _resolve_timezone(tz)
    if dt is None:
        dt = datetime.now(timezone.utc)
    elif isinstance(dt, t.struct_time):
        dt = datetime.fromtimestamp(t.mktime(dt), tz=timezone.utc)
    elif isinstance(dt, DateTime):  # legacy Zope implementation, returned e.g. by ZopeTime()
        dt = datetime.fromisoformat(dt.ISO8601())
    elif isinstance(dt, date) and not isinstance(dt, _DATETIME_TYPE):
        dt = datetime.combine(dt, datetime.min.time())
    elif isinstance(dt, time):
        dt = datetime.combine(datetime.now(target_timezone).date(), dt)
    if not isinstance(dt, _DATETIME_TYPE):
        raise TypeError(f'Unsupported datetime value: {type(dt).__name__}')
    dt = _attach_timezone(dt, target_timezone)
    if days_delta:
        dt += timedelta(days=days_delta)
    return dt.astimezone(target_timezone)


print('Helper: zms.unibe.helpers.datetime.get_when')
@security.public
def get_when(dt: Any = None,
             mode: str | None = None,
             locale: str = 'de_CH',
             tz: str | tzinfo | None = None,
             granularity: str = 'second',
             threshold: float | int = 0.85,
             format: str = 'long',
             add_direction: bool = True) -> str | float:
    """
    Format a date/time value or relative duration using Babel.

    ``date``, ``time``, ``day``, and ``weekday`` select localized calendar
    representations; ``utcoffset`` returns the offset in hours. ``delta``
    formats a timedelta or a number interpreted as days. A timedelta always
    selects ``delta`` mode. Other string modes are Babel datetime patterns;
    ``None``, ``iso``, and ``iso8601`` use the default ISO8601 pattern.

    :param dt: A datetime, date, time, ISO8601 string, timedelta, or numeric
        value interpreted as days in ``delta`` mode. ``None`` means the current time.
    :param mode: Formatting mode, Babel datetime pattern, or ``None`` for ISO8601.
    :param locale: Babel locale identifier.
    :param tz: Target IANA timezone or tzinfo. If omitted, an aware input
        supplies its timezone; otherwise ``Europe/Zurich`` is used.
    :param granularity: Smallest unit used by Babel for ``delta`` mode.
    :param threshold: Babel's threshold for stepping to the next duration unit.
    :param format: Babel duration format, such as ``long`` or ``short``.
    :param add_direction: Whether delta output includes relative direction.
    :return: Formatted text, or the UTC offset in hours for ``utcoffset`` mode.
    """
    if isinstance(dt, timedelta):
        mode = 'delta'

    if mode == 'delta':
        if not isinstance(dt, timedelta):
            try:
                dt = timedelta(days=dt)
            except TypeError:
                dt = timedelta(days=0)
        return format_timedelta(dt,
                                locale=locale,
                                granularity=granularity,
                                threshold=threshold,
                                format=format,
                                add_direction=add_direction)

    if tz is None:
        source_timezone = getattr(dt, 'tzinfo', None)
        if isinstance(dt, str):
            try:
                source_timezone = datetime.fromisoformat(dt).tzinfo
            except ValueError:
                pass
        tz = source_timezone or DEFAULT_TIMEZONE
    try:
        target_timezone = _resolve_timezone(tz)
    except (LookupError, TypeError):
        target_timezone = ZoneInfo(DEFAULT_TIMEZONE)

    match mode:
        case 'date':
            return format_date(local_timezone(dt, tz=target_timezone),
                               format='long',
                               locale=locale)
        case 'time':
            return format_time(local_timezone(dt, tz=target_timezone),
                               format='short',
                               locale='de',  # enforce 24h format to avoid AM/PM
                               tzinfo=target_timezone)
        case 'day':
            return format_date(local_timezone(dt, tz=target_timezone),
                               format='d',
                               locale=locale)
        case 'weekday':
            return format_date(local_timezone(dt, tz=target_timezone),
                               format='E',
                               locale=locale).replace('.', '')
        case 'utcoffset':
            return local_timezone(dt, tz=target_timezone).utcoffset().total_seconds() / 3600
        case x if x not in (None, 'iso', 'iso8601'):
            # https://babel.pocoo.org/en/latest/dates.html#pattern-syntax
            return format_datetime(local_timezone(dt, tz=target_timezone),
                                   format=mode,
                                   locale=locale,
                                   tzinfo=target_timezone)
    # return ISO8601 format as default
    return format_datetime(local_timezone(dt, tz=target_timezone),
                           format="yyyy-MM-dd'T'HH:mm:ssZZZZZ",
                           locale=locale,
                           tzinfo=target_timezone)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
