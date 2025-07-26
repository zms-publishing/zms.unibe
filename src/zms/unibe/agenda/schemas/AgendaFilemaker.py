from babel.dates import format_date, format_datetime, format_time
from zms.unibe.utils.helpers import local_timezone
import logging

LOGGER = logging.getLogger('AgendaFilemaker')


def mapping(item, locale):
    event = {
        'eventId': None,  # n/a
        'eventSource': 'agenda_filemaker',
        'eventTitle': item.veranstaltung_titel,

        'eventStartDateTime': get_event_when(item.json_datum_zeit_start, 'iso', locale),
        'eventStartDate': get_event_when(item.json_datum_zeit_start, 'date', locale),
        'eventStartTime': get_event_when(item.json_datum_zeit_start, 'time', locale),
        'eventStartDay': get_event_when(item.json_datum_zeit_start, 'day', locale),
        'eventStartDayWeek': get_event_when(item.json_datum_zeit_start, 'weekday', locale),

        'eventEndDateTime': get_event_when(item.json_datum_zeit_end, 'iso', locale),
        'eventEndDate': get_event_when(item.json_datum_zeit_end, 'date', locale),
        'eventEndTime': get_event_when(item.json_datum_zeit_end, 'time', locale),
        'eventEndDay': get_event_when(item.json_datum_zeit_end, 'day', locale),
        'eventEndDayWeek': get_event_when(item.json_datum_zeit_end, 'weekday', locale),

        'eventLocation': get_event_where(item),
        'eventInfos': get_event_what(item),
        'eventTopics': None,  # n/a
        'eventImage': None,  # n/a
        'eventUrl': item.veranstalter_info_link,
    }
    return event


def get_event_when(dt, mode, locale):
    try:
        val = local_timezone(dt)
    except (ValueError, TypeError):
        LOGGER.error(f'Error parsing date/time: {dt} -> mapped to 2099-12-31 12:12')
        val = local_timezone('2099-12-31 12:12')  # broken DateTimes -> 31 Dec 2099 12:12

    # https://babel.pocoo.org/en/latest/dates.html#pattern-syntax
    if mode == 'date':
        return format_date(val, format='long', locale=locale)
    elif mode == 'time':
        return format_time(val, format='short', locale=locale)
    elif mode == 'day':
        return format_date(val, format='d', locale=locale)
    elif mode == 'weekday':
        return format_date(val, format='E', locale=locale)

    return val  # datetime will be transformed to ISO on JSON export


def get_event_where(item):
    str = f'{item.veranstaltung_horsaal} {item.veranstaltung_gebaude_adresse}'
    return str


def get_event_what(item):
    str = f'{item.veranstaltung_referenten} {item.veranstaltung_zyklus}'
    return str
