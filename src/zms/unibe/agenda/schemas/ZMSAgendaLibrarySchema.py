from uuid import uuid4
from zms.unibe.utils.helpers import local_timezone, get_when


class ZMSAgendaLibrarySchema:
    def mapping(self, event, locale):
        begin = local_timezone(event.startsAt)
        end = local_timezone(event.endsAt)

        return {
            'eventId': str(uuid4()),  # temporary UUID until next import - for internal use only
            'eventSource': 'agenda_library',
            'eventTitle': event.title,
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

            'eventLocation': event.venue,
            'eventInfos': "",  # TODO: render infos as html in popup overlay
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': event.subjects,  # TODO: display categories and provide filter
            'eventImage': event.imageUrl,
            'eventUrl': event.url,
        }