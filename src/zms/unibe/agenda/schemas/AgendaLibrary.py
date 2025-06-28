# TODO: Map items from UB-Agenda as Backend -> see schemas/README.md

from zms.unibe.utils.helpers import local_timezone

def mapping(item):
    event = {
        'eventId': None,
        'eventSource': 'agenda_library',
        'eventTitle': item['title'],
        'eventStart': local_timezone(item['startsAt']),
        'eventEnd': local_timezone(item['endsAt']),
        'eventLocation': item['venue'],
        'eventInfos': item['eventType'],
        'eventTopics': item['subjects'],
        'eventImage': item['imageUrl'],
        'eventUrl': item['url'],
    }
    return event
