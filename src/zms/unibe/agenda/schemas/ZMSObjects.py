# TODO: Map attributes from ZMS as Backend -> see schemas/README.md
# TODO: Limit UniBEEvent to only active ones from ZMS as Backend
# TODO: Limit TeaserElement2022 to (teaser_type==event) from ZMS as Backend
# TODO: Limit NewsBox to (boxtype==event) from ZMS as Backend

from zms.unibe.utils.helpers import local_timezone

def mapping(item, meta_id, lang, obj=None):
    if meta_id == 'ZMSAgendaRecordset':
        event = {
            'eventId': item.get('eventId'),
            'eventSource': obj.agenda_recordset.getPath(),
            'eventTitle': item.get('eventTitle'),
            'eventStart': local_timezone(item.get('eventStart')),
            'eventEnd': local_timezone(item.get('eventEnd')),
            'eventLocation': item.get('eventLocation'),
            'eventInfos': item.get('eventInfos'),
            'eventTopics': item.get('eventTopics').split(),
            'eventImage': str(item.get('eventImage')),
            'eventUrl':obj.getLinkObj(item.get('eventUrl')).getPath() if obj.getLinkObj(item.get('eventUrl'))
                                                                         is not None else None,
        }
    else:
        event = {
            'eventId': item.get_uid().replace('uid:', 'urn:uuid:'),
            'eventSource': item.getPath(),
            'eventTitle': item.getTitle(REQUEST={'lang': lang}),
            'eventStart': local_timezone(),
            'eventEnd': local_timezone(),
            'eventLocation': 'location',
            'eventInfos': 'infos',
            'eventTopics': ['topics'],
            'eventImage': 'image',
            'eventUrl': 'url',
        }
    return event
    