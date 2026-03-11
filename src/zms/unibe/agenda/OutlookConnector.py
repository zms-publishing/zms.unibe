# OutlookConnector accesses calendars and events using the Microsoft Graph API
# https://learn.microsoft.com/en-us/graph/api/resources/calendar-overview?view=graph-rest-1.0

import asyncio
import json
import requests
import base64
import logging
from dotenv import load_dotenv
from azure.identity import EnvironmentCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.events.item.attachments.attachments_request_builder import AttachmentsRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration

from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager  # inherit from to use ClassSecurityInfo

from Products.zms.standard import pybool
from zms.unibe.utils.helpers import DotDict, local_timezone
from zms.unibe.agenda.schemas.ZMSAgendaOutlookSchema import ZMSAgendaOutlookSchema

print('Addon: zms.unibe.agenda.OutlookConnector')
security = ModuleSecurityInfo('zms.unibe.agenda.OutlookConnector')  # allow module import in RestrictedPython

LOGGER = logging.getLogger('OutlookConnector')

load_dotenv()


class OutlookConnector(ObjectManager):
    credential: EnvironmentCredential
    graph_client: GraphServiceClient

    security = ClassSecurityInfo()  #  control access to class methods in RestrictedPython

    def __init__(self, upn):
        self.upn = upn
        self.credential = EnvironmentCredential()
        self.graph_client = GraphServiceClient(self.credential)  # type: ignore
        self.headers = {
            'Authorization': 'Bearer ' + asyncio.run(self.get_access_token()),
            'Prefer': 'IdType="ImmutableId",'  # https://learn.microsoft.com/en-us/graph/outlook-immutable-id
                      'outlook.timezone="Europe/Berlin"',  # https://learn.microsoft.com/en-us/graph/api/user-list-events?view=graph-rest-1.0&tabs=http#support-various-time-zones
        }
        
    async def get_access_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = self.credential.get_token(graph_scope)
        
        return access_token.token

    def get_calendar_events(self, begin_date, end_date):
        """
        Fetch calendar events of the set UPN in the given time range.

        The events retrieved are filtered to include either the events organized by
        the set UPN or the events accepted by the set UPN following an invitation.

        If the event is an invitation accepted by the set UPN, the organizer's name
        is removed from the event subject.

        Events shown as tentative are not included in the result.

        The events are retrieved via the Microsoft Graph API using specific query parameters,
        such as ensuring the correct timezone is applied and limiting the number of events.

        Returns:
            str: A JSON string containing the list of events filtered for the
                 set UPN on specific criteria.

        Raises:
            ValueError: If the API response contains an error or invalid data.
        """
        # /calendar/events?$top=100
        # /calendar/events?mailboxlocation=resource
        # /calendarView?startDateTime=2023-07-26T00:00:00Z&endDateTime=2026-07-27T00:00:00Z
        # /calendarView -> max time range is 5 years
        # /calendarView -> unfolds recurring event settings to multiple event occurrences in the set behaviour
        # https://learn.microsoft.com/en-us/graph/api/user-list-calendarview?view=graph-rest-1.0&tabs=http
        response = requests.get(url=f"https://graph.microsoft.com/v1.0"
                                    f"/users/{self.upn}/calendarView"
                                    f"?startDateTime={local_timezone(begin_date, tz='UTC').isoformat()[:-6]}"
                                    f"&endDateTime={local_timezone(end_date, tz='UTC', days_delta=1).isoformat()[:-6]}"
                                    f"&$top=100",
                                headers=self.headers)
        response_json = response.json()

        return_json = []
        # TODO: rewrite using https://learn.microsoft.com/en-us/graph/filter-query-parameter?tabs=http
        # TODO: rewrite using https://learn.microsoft.com/en-us/graph/api/calendar-list-events?view=graph-rest-1.0&tabs=python
        if "value" in response_json:
            data = response_json["value"]
            for event in data:
                event = DotDict(event)
                if event.organizer.emailAddress.address == self.upn:
                    if event.showAs != 'tentative':
                        return_json.append(event)
                else:
                    for attendee in event.attendees:
                        attendee = DotDict(attendee)
                        if attendee.emailAddress.address == self.upn:
                            if attendee.status.response == 'accepted':
                                event.subject = event.subject.replace(event.organizer.emailAddress.name, '').strip()
                                if event.showAs != 'tentative':
                                    return_json.append(event)
            return json.dumps(return_json, indent=4, sort_keys=True)

        LOGGER.error(response_json)
        raise ValueError(response_json)

    @security.public
    def debug_calendar_events(self, begin_date, end_date, events_endpoint=None,
                                     event_id=None, attachment_id=None, decode_base64=False):
        if pybool(events_endpoint):
            response = requests.get(url=f"https://graph.microsoft.com/v1.0"
                                        f"/users/{self.upn}/events"
                                        f"?$top=100",
                                    headers=self.headers)
            return json.dumps(response.json(), indent=4, sort_keys=True)

        if event_id is not None:
            if attachment_id is not None:
                rtn = self.get_event_attachments(event_id, attachment_id, decode_base64)
                if isinstance(rtn, list):
                    return json.dumps(rtn, indent=4, sort_keys=True, default=str)
                return rtn
            else:
                response = requests.get(url=f"https://graph.microsoft.com/v1.0"
                                            f"/users/{self.upn}/events/{event_id}",
                                        headers=self.headers)
                return json.dumps(response.json(), indent=4, sort_keys=True)

        response = requests.get(url=f"https://graph.microsoft.com/v1.0"
                                    f"/users/{self.upn}/calendarView"
                                    f"?startDateTime={local_timezone(begin_date, tz='UTC').isoformat()[:-6]}"
                                    f"&endDateTime={local_timezone(end_date, tz='UTC', days_delta=1).isoformat()[:-6]}"
                                    f"&$top=100",
                                headers=self.headers)
        return json.dumps(response.json(), indent=4, sort_keys=True)

    @security.public
    def debug_calendar_categories(self):
        # TODO: FindCategoriesAccessDenied
        # With _delegated_ permission MailboxSettings.Read* you can't read/write outlook categories of other users.
        # Only way to read/write outlook categories is with _application_ permission MailboxSettings.ReadWrite.
        # With this application permission, you can limit the scope to a subset of mailboxes.
        # https://stackoverflow.com/questions/77825238/get-create-categories-for-any-user-in-outlook-calendar-with-graphapi
        response = requests.get(url=f"https://graph.microsoft.com/v1.0"
                                    f"/users/{self.upn}/outlook/masterCategories",
                                headers=self.headers)
        return json.dumps(response.json(), indent=4, sort_keys=True)                              

    @security.public
    def get_event_attachments(self, event_id=None, attachment_id=None, decode_base64=False):
        """
        Retrieve event attachments and their data.

        This method is designed to fetch attachments belonging to a specified event. If an attachment ID is not provided,
        it retrieves a list of all available attachments for the given event. If an attachment ID is provided, it retrieves
        the specific attachment's data. Attachments can also be optionally decoded from base64 format.

        Parameters:
            event_id: str
                The ID of the event for which attachments are to be retrieved. This parameter is required.
            attachment_id: Optional[str]
                The ID of the specific attachment to retrieve. If not provided, all attachments for the
                specified event will be retrieved.
            decode_base64: bool
                When True, the method will decode the content of the attachment from base64 format. Defaults to False.

        Returns:
            list | tuple
                Returns a list of attachments for the event if no attachment ID is provided. Each attachment is
                a dictionary containing details such as ID, content type, name, size, inline status, and last
                modified time. If an attachment ID is specified, a tuple containing the attachment name and its
                content (optionally decoded) is returned.

        Raises:
            AssertionError
                Raised if the `event_id` parameter is not provided.
        """
        assert event_id is not None, 'event_id is required'

        # retrieve available attachments of an event
        if attachment_id is None:
            attachment_list = []
            query_params = AttachmentsRequestBuilder.AttachmentsRequestBuilderGetQueryParameters(
                #select=["id", "content_id", "contentType", "name", "size", "isInline", "lastModifiedDateTime"],
                # -> could not find a property named 'content_id' on type 'microsoft.graph.attachment'
                # -> also 'cid' or 'contentId' or 'microsoft.graph.fileattachment/contentId' do not work
            )
            request_config = RequestConfiguration(
                query_parameters=query_params,
            )
            
            # When making client calls from a sync env with asyncio.run() the loop 
            # gets closed after the first request, causing subsequent ones to fail
            # https://github.com/microsoftgraph/msgraph-sdk-python/issues/366
            # -> see workaround
            def get_loop():
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                return loop
            
            attachments = get_loop().run_until_complete(self.graph_client.users.by_user_id(self.upn).events.by_event_id(
                event_id).attachments.get(request_configuration=request_config))

            return attachments.value

        # retrieve attachment data of an event
        attachment_data = asyncio.run(self.graph_client.users.by_user_id(self.upn).events.by_event_id(
            event_id).attachments.by_attachment_id(
            attachment_id).get())
        if decode_base64:
            # https://stackoverflow.com/questions/76705913/download-raw-content-of-email-attachment-using-microsoft-graph-sdk
            return attachment_data.name, base64.urlsafe_b64decode(attachment_data.content_bytes)
        else:
            return attachment_data.name, attachment_data.content_bytes

    @security.public
    def create_calendar_event(self, data):   
        data = DotDict(data)
        payload = ZMSAgendaOutlookSchema.from_surveyjs(data)
        
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        
        response = requests.post(url=f"https://graph.microsoft.com/v1.0"
                                     f"/users/{self.upn}/calendar/events",
                                 headers=headers,
                                 json=payload)
        
        # print('create_calendar_event -> POST:', self.upn,
        #       json.dumps(payload, indent=4, sort_keys=True, default=str),
        #       response.status_code,
        #       response.text)
        
        if response.status_code != 201:
            LOGGER.error(f'POST {self.upn} {response.status_code} {response.text}')
            raise ValueError(
                f"Failed to create calendar event for {self.upn}: "
                f"{response.status_code} {response.text}")
        
        try:
            return response.json()
        except Exception:
            LOGGER.warning(
                f"create_calendar_event: successful response for {self.upn} "
                f"could not be decoded as JSON (status {response.status_code})")
            return {"status_code": response.status_code}
        

# Apply security assertions by ClassSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#a-class-security-example
InitializeClass(OutlookConnector)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
