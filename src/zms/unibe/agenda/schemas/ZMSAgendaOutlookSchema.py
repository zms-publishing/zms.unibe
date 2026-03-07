from bs4 import BeautifulSoup
from Products.zms import standard
from zms.unibe.utils.helpers import local_timezone, get_when, sanitize_html
import datetime as dt


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
        # remove editorial notes from rendering
        for tag in soup.find_all('blockquote'):
            tag.decompose()
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
            'eventInfosPreview': None,  # preview,  -> removed due to leading editorial notes in <blockquote>
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
    
    @classmethod
    def from_surveyjs(cls, event):

        # we expect a lead time of one day for new events 
        tomorrow = local_timezone() + dt.timedelta(days=1)
        begin_date = local_timezone(event.event_begin_date)

        if 'event_end_date' in event:
            end_date = local_timezone(event.event_end_date)
        else:
            end_date = tomorrow

        if 'event_begin_time' in event:
            begin_time = dt.time.fromisoformat(event.event_begin_time)
        else:
            begin_time = dt.time.fromisoformat(tomorrow.strftime('%H:%M:%S'))

        if 'event_end_time' in event:
            end_time = dt.time.fromisoformat(event.event_end_time)
        else:
            end_time = dt.time.fromisoformat(tomorrow.strftime('%H:%M:%S'))

        if 'allday' in event.event_duration:
            begin_time = dt.time.fromisoformat('00:00:00')
            end_time = dt.time.fromisoformat('00:00:00')

        begin_datetime = dt.datetime.combine(begin_date, begin_time, tzinfo=tomorrow.tzinfo)
        end_datetime = dt.datetime.combine(end_date, end_time, tzinfo=tomorrow.tzinfo)

        if begin_datetime < tomorrow:
            begin_datetime = end_datetime

        if end_datetime < begin_datetime:
            end_datetime = begin_datetime

        if begin_datetime == end_datetime:
            end_datetime = end_datetime + dt.timedelta(days=1)

        if event.get('event_link', '').startswith('https://'):
            link = f"<a href='{event.get("event_link")}' target='_blank'>{event.get("event_link")[8:]}</a>"
        else:
            link = ""

        if event.get('event_categories'):
            if isinstance(event.event_categories, list):
                categories = event.event_categories.copy()
            else:
                categories = [event.event_categories]
            if 'other' in categories:
                categories.remove('other')
        else:
            categories = []

        return {
            "showAs": "tentative",
            "subject": event.event_title,
            "body": {
                "contentType": "HTML",
                "content": f"<blockquote style=\"margin-left:0.8ex; padding-left:1ex; border-left:3px solid rgb(200,200,200); color:rgb(102,102,102)\">"
                           f"KONTAKT: {event.get('event_submitter_name', '')}"
                    f"<br />{event.get('event_submitter_email', '')} {event.get('event_submitter_phone', '')}"
                    f"<hr />BEACHTE: {event.get('event_submitter_hints', '')}"
                    f"<hr />TURNUS: {event.get('event_recurrence', '')}"
                    f"<hr />WEITERE KATEGORIE: {event.get('event_categories-Comment', '')}"
                    f"<hr /></blockquote><br />{event.get('event_description', '')} {link}"
            },
            "isAllDay": True if 'allday' in event.event_duration else False,
            "start": {
                "dateTime": begin_datetime.isoformat()[:-6],
                "timeZone": "Europe/Berlin"
            },
            "end": {
                "dateTime": end_datetime.isoformat()[:-6],
                "timeZone": "Europe/Berlin"
            },
            "location": {
                "displayName": event.event_location
            },
            "categories": categories,
            # "attendees": [
            #     {
            #         "emailAddress": {
            #             "address": event.event_submitter_email,
            #             "name": event.event_submitter_name
            #         },
            #         "type": "optional"
            #     },
            # ],
            # => 403 {"error":{"code":"ErrorAccessDenied"}}
        }
