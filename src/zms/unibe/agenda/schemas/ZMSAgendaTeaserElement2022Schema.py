from Products.zms import _blobfields
from zms.unibe.utils.helpers import local_timezone, get_when


class ZMSAgendaTeaserElement2022Schema:
    def mapping(self, event, context, lang, locale):
        if event.attr('teaser_type') != 'event':
            return None

        begin = local_timezone(event.attr('event_date_start', REQUEST={'lang': lang}))
        end = local_timezone(event.attr('event_date_end', REQUEST={'lang': lang}))

        return {
            'eventId': event.get_uid().replace('uid:', ''),
            'eventSource': event.getPath(),
            'eventTitle': event.attr('title'),
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

            'eventLocation': event.attr('event_location'),
            'eventInfos': event.attr('text'),
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': event.attr('topic').split('\r\n'),
            'eventImage': event.attr('img').getHref(REQUEST={'lang': lang}) if isinstance(event.attr('img'),
                                                                                          _blobfields.MyImage) else None,
            'eventUrl': context.getLinkUrl(event.attr('url'), REQUEST={'lang': lang}),
        }
