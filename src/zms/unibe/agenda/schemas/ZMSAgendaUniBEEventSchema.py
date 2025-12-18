from Products.zms import _blobfields
from zms.unibe.utils.helpers import local_timezone, get_when


class ZMSAgendaUniBEEventSchema:
    # TODO: adjust UniBEEvent mapping
    def mapping(self, event, context, lang, locale):

        begin = local_timezone(event.attr('eventStart', REQUEST={'lang': lang}))
        end = local_timezone(event.attr('eventEnd', REQUEST={'lang': lang}))

        return {
            'eventId': event.get_uid().replace('uid:', ''),
            'eventSource': event.getPath(),
            'eventTitle': event.getTitle(REQUEST={'lang': lang}),
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

            'eventLocation': event.attr('eventAreal_Gebaeude', REQUEST={'lang': lang}),
            'eventInfos': event.attr('eventText', REQUEST={'lang': lang}),
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': event.attr('attr_dc_subject', REQUEST={'lang': lang}).split('\r\n'),
            'eventImage': event.attr('titleimage', REQUEST={'lang': lang}).getHef(REQUEST={'lang': lang}) if isinstance(
                event.attr('titleimage', REQUEST={'lang': lang}), _blobfields.MyImage) else None,
            'eventUrl': context.getLinkUrl(event.attr('eventUrl'), REQUEST={'lang': lang}),
        }