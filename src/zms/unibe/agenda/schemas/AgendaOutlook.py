# TODO: Map calendar/events from Outlook as Backend -> see schemas/README.md

from zms.unibe.utils.helpers import local_timezone

def mapping(item):
    event = {
        'eventId': None,
        'eventSource': 'agenda_outlook',
        'eventTitle': item['subject'],
        'eventStart': local_timezone(item['start']['dateTime']),
        'eventEnd': local_timezone(item['end']['dateTime']),
        'eventLocation': 'location',
        'eventInfos': str(item['body']['content']),
        'eventTopics': item['categories'],
        'eventImage': 'image',
        'eventUrl': 'url',
    }
    return event
    