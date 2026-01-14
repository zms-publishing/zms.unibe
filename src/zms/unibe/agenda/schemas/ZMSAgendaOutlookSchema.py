from bs4 import BeautifulSoup
from Products.zms import standard
from zms.unibe.utils.helpers import local_timezone, get_when, sanitize_html


class ZMSAgendaOutlookSchema:
    def mapping(self, event, attachments, account, locale):

        begin = local_timezone(event.start.dateTime)
        end = local_timezone(event.end.dateTime)

        if event.isAllDay:
            # Outlook sets the end date to midnight (00:00) of the next day
            # if all-day is set, which means there are no start/end times.
            # Therefore, we need to adjust it to get the actual end date.
            end = local_timezone(end, days_delta=-1)
        
        # extract the last hyperlink
        # -> check below if the link is the only content
        # -> render as a direct link without a modal overlay
        href = sanitize_html(event.body.content, 'href')
        href = href if href.startswith('http') else None
        
        preview = sanitize_html(event.bodyPreview)
        content = sanitize_html(event.body.content)

        # make all links open in a new tab
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a'):
            link['target'] = '_blank'
        content = str(soup)

        return {
            'eventId': event.id,
            'eventSource': account,
            'eventTitle': event.subject,
            'eventAttachments': attachments,
            'eventAllDay': event.isAllDay,

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

            'eventLocation': event.location.displayName,  # TODO: handle geo-coords and multiple locations...?!
            'eventInfos': content if preview != href else '',  # if plain link set as eventUrl below and leave infos empty
            'eventInfosPreview': preview,
            'eventTagline': None,
            'eventCategories': event.categories,
            'eventImage': None,  # TODO: handle inline images - /event/body.content contains binary...?!
            'eventUrl': href if preview == href else None,
        }

    def mapping_attachment(self, attachment):
        return {
            'id': attachment.id,
            'contentId': attachment.content_id,  # TODO: needed to identify inline images by cid: to get bytes data...?!
            'contentType': attachment.content_type,
            'name': attachment.name,
            'size': attachment.size,
            "isInline": attachment.is_inline,
            'lastModifiedDateTime': attachment.last_modified_date_time,
            'fileExtension': attachment.content_type.split('/')[-1] if '/' in attachment.content_type else None,
            'fileSize': standard.getDataSizeStr(attachment.size),
        }
