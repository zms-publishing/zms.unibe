# Access Outlook in M365 cloud
# see Working with calendars and events using the Microsoft Graph API
# https://learn.microsoft.com/en-us/graph/api/resources/calendar-overview?view=graph-rest-1.0

import json
import requests
import base64
import logging
from devtools import debug
from dotenv import load_dotenv
from azure.identity import EnvironmentCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.events.item.attachments.attachments_request_builder import AttachmentsRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration

from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager  # inherit from to use ClassSecurityInfo

print('Addon: zms.unibe.agenda.OutlookConnector')
security = ModuleSecurityInfo('zms.unibe.agenda.OutlookConnector')  # allow module import in RestrictedPython

LOGGER = logging.getLogger('OutlookConnector')

load_dotenv()


class OutlookConnector(ObjectManager):
    credential: EnvironmentCredential
    graph_client: GraphServiceClient

    security = ClassSecurityInfo()  #  control access to class methods in RestrictedPython

    def __init__(self, account):
        self.account = account
        self.credential = EnvironmentCredential()
        self.graph_client = GraphServiceClient(self.credential)  # type: ignore
        
    async def get_access_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = self.credential.get_token(graph_scope)
        
        return access_token.token

    async def get_calendar_events(self):
        headers = {
            'Authorization': 'Bearer ' + await self.get_access_token(),
            'Prefer': 'IdType="ImmutableId",'  # https://learn.microsoft.com/en-us/graph/outlook-immutable-id
                      'outlook.timezone="Europe/Berlin"',  # https://learn.microsoft.com/en-us/graph/api/user-list-events?view=graph-rest-1.0&tabs=http#support-various-time-zones
        }
        # /calendar/events?$top=100
        # /calendar/events?mailboxlocation=resource
        # /calendarView?startDateTime=2023-07-26T00:00:00Z&endDateTime=2023-07-27T00:00:00Z
        response = requests.get(url=f"https://graph.microsoft.com/v1.0/users/{self.account}/calendar/events?$top=100",
                                headers=headers)
        response_json = response.json()

        if "value" in response_json:
            return json.dumps(response_json["value"], indent=4, sort_keys=True)

        LOGGER.log(logging.ERROR, response_json)
        raise ValueError(response_json)

    @security.public
    async def get_calendar_attachments(self, attachment_id=None, raw_data=False):
        # TODO: remove hardcoded form POC -> implement this feature 
        query_params = AttachmentsRequestBuilder.AttachmentsRequestBuilderGetQueryParameters(
            select=["id", "contentType", "name", "size", "lastModifiedDateTime"],
        )
        request_config = RequestConfiguration(
            query_parameters=query_params,
        )
        debug(await self.graph_client.users.by_user_id(self.account).events.by_event_id(
            'AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A3NJhpCaVKU2JrM7AyoUylgAAAABPoQAA').attachments.get(
            request_configuration=request_config))

        data = await self.graph_client.users.by_user_id(self.account).events.by_event_id(
            'AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A3NJhpCaVKU2JrM7AyoUylgAAAABPoQAA').attachments.by_attachment_id(
            attachment_id).get()
        if raw_data:
            # https://stackoverflow.com/questions/76705913/download-raw-content-of-email-attachment-using-microsoft-graph-sdk
            return base64.urlsafe_b64decode(data.content_bytes)
        else:
            return data.name


# Apply security assertions by ClassSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#a-class-security-example
InitializeClass(OutlookConnector)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
