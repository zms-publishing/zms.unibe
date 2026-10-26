from ...utils.helpers import flatten_to_str_list, get_when, local_timezone, normalize_split_by

class ZMSAgendaRecordsetSchema:
    def mapping(self, event, context, lang, locale):
        
        begin = local_timezone(event.eventBegin)
        end = local_timezone(event.eventEnd)
        categories = flatten_to_str_list(normalize_split_by(event.eventCategories))

        event_infos = f'{event.eventInfos or ""}'.strip()
        event_url = context.getLinkUrl(event.eventUrl, REQUEST={'lang': lang})
        if event_url and event_url.startswith('http'):
            event_infos = (f'{event_infos} <p><a href="{event_url}"'
                           f' target="_blank">{event_url}</a></p>') if event_infos != '' else event_infos

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
            'eventInfos': event_infos,
            'eventInfosPreview': None,
            'eventTagline': None,
            'eventCategories': categories,
            'eventImage': None,  # n/a
            'eventUrl': event_url,
        }
