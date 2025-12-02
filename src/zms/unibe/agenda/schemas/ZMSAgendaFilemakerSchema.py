from uuid import uuid4
from zms.unibe.utils.helpers import local_timezone, get_when


class ZMSAgendaFilemakerSchema:
    def mapping(self, event, locale):
        begin = local_timezone(event.json_datum_zeit_start)
        end = local_timezone(event.json_datum_zeit_end)

        return {
            'eventId': str(uuid4()),  # temporary UUID until next import - for internal use only
            'eventSource': 'agenda_filemaker',
            'eventTitle': event.veranstaltung_titel,
            'eventAttachments': None,
            'eventAllDay': False,  # begin.date() != end.date(),

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

            'eventLocation': f'{event.veranstaltung_gebaude_adresse} {event.veranstaltung_horsaal}',
            'eventInfos': f'',  # {event.veranstaltung_referenten}
            'eventInfosPreview': None,
            'eventTagline': f'{event.veranstaltung_zyklus}',
            'eventCategories': None,  # n/a
            'eventImage': None,  # n/a
            'eventUrl': event.veranstalter_info_link,
        }
