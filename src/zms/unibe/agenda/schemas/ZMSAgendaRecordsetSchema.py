from zms.unibe.utils.helpers import local_timezone, get_when


class ZMSAgendaRecordsetSchema:
    def mapping(self, event, context, lang, locale):
        begin = local_timezone(event.eventBegin)
        end = local_timezone(event.eventEnd)

        return {
            'eventId': event.get('eventId'),
            'eventSource': context.agenda_recordset.getPath(),
            'eventTitle': event.get('eventTitle'),
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

            'eventLocation': event.eventLocation,
            'eventInfos': event.eventInfos,
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': event.eventCategories.split('\r\n'),  # TODO: check if linebreak is safe for Windows...?!
            'eventImage': None,  # n/a
            'eventUrl': context.getLinkUrl(event.eventUrl, REQUEST={'lang': lang}),
        }
