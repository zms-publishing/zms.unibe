# TODO: Map items from FileMaker as Backend -> see schemas/README.md

from ..helpers import local_timezone

def mapping(item):
    event = {
        'eventId': None, 
        'eventSource': 'agenda_filemaker',
        'eventTitle': item['veranstaltung_titel'],
        'eventLocation': (item['veranstaltung_horsaal']
                          + item['veranstaltung_gebaude_adresse']),
        'eventInfos': (item['veranstaltung_referenten']
                       + item['veranstaltung_zyklus']),
        'eventTopics': None,
        'eventImage': None,
        'eventUrl': item['veranstalter_info_link'],
    }
    try:
        event['eventStart'] = local_timezone(item['json_datum_zeit_start'])
        event['eventEnd'] = local_timezone(item['json_datum_zeit_end'])
    except (ValueError, TypeError):
        return None
    return event
