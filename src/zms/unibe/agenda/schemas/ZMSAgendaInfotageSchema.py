import re
from uuid import uuid4
from zms.unibe.utils.helpers import local_timezone, get_when


def _extract_href(value):
    """Return (plain_url, original_html) from an <a href="..."> string.
    If value is not an anchor tag, returns (value, None)."""
    match = re.search(r'href\s*=\s*["\']([^"\']+)["\']', value or '', re.IGNORECASE)
    if match:
        return match.group(1), value
    return value, None


class ZMSAgendaInfotageSchema:
    def mapping(self, event, locale):
        begin = local_timezone(event.eventBeginDateTime)
        end = local_timezone(event.eventEndDateTime)

        plain_url, href_html = _extract_href(event.eventUrl)
        event_infos = f'{event.eventInfos}'
        if href_html:
            event_infos = f'{event_infos} <p>{href_html}</p>'.strip() if event_infos != '' else event_infos

        return {
            'eventId': str(uuid4()),  # temporary UUID until next import - for internal use only
            'eventSource': 'agenda_infotage',
            'eventTitle': event.eventTitle,
            'eventAttachments': None,
            'eventAllDay': begin.date() != end.date(),

            'eventBeginDateTime': get_when(begin, 'iso', locale),
            'eventBeginDate': get_when(begin, 'date', locale),
            'eventBeginTime': get_when(begin, 'time', locale),
            'eventBeginDay': get_when(begin, 'day', locale),
            'eventBeginDayWeek': get_when(begin, 'weekday', locale),

            'eventEndDateTime': get_when(end, 'iso', locale),
            'eventEndDate': get_when(end, 'date', locale),
            'eventEndTime': get_when(end, 'time', locale),
            'eventEndDay': get_when(end, 'day', locale),
            'eventEndDayWeek': get_when(end, 'weekday', locale),

            'eventLocation': f'{event.eventLocation}',
            'eventInfos': event_infos,
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': event.eventCategories,
            'eventImage': None,  # n/a
            'eventUrl': plain_url,
        }
