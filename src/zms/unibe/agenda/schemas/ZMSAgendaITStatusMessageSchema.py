from zms.unibe.utils.helpers import local_timezone, get_when


class ZMSAgendaITStatusMessageSchema:
    def mapping(self, event, locale):

        begin = local_timezone(event.begin)
        # set the end date to next week if none is specified to ongoing outage
        end = local_timezone(days_delta=7) if event.end is None else local_timezone(event.end)

        return {
            'eventId': event.id,
            'eventSource': 'agenda_itstatusmessages',
            'eventTitle': event.subject,
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

            'eventLocation': None,
            'eventInfos': f"{event.description} {event.service} {event.info}",
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': event.type.split('\r\n'),
            'eventImage': None,
            'eventUrl': None,
        }
