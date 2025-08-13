# AgendaBridge aggregates events from different data sources
# see also sqlmodels/__main__.py to store in PostgreSQL for unibe.app

import asyncio
import requests
import json
import logging

from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager  # inherit from to use ClassSecurityInfo
from ZTUtils.Lazy import LazyMap
from operator import attrgetter
from ics import Calendar, Event

from ..utils.helpers import DotDict, local_timezone
from .OutlookConnector import OutlookConnector


print('Addon: zms.unibe.agenda.AgendaBridge')
security = ModuleSecurityInfo('zms.unibe.agenda.AgendaBridge')  # allow module import in RestrictedPython

LOGGER = logging.getLogger('ZMSAgenda')


class AgendaBridge(ObjectManager):
    security = ClassSecurityInfo()  # control access to class methods in RestrictedPython
    
    def __init__(self, locale, start_date=None, end_date=None, categories=None):
        self.events = []
        self.locale = locale
        self.start_date = local_timezone(start_date)
        self.end_date = local_timezone(end_date)
        self.categories = categories

    @security.public    
    def get_events(self, mode=None):
        array = [x.model_dump() for x in sorted(
            self.events,
            key=attrgetter('eventStartDateTime', 'eventEndDateTime')
        )]

        # filter out events without the given categories
        if isinstance(self.categories, list) and len(self.categories) > 0:
            prefix = 'ZMSAgenda.Category.'
            array_filtered = []
            for category in self.categories:
                category = category.replace(prefix, '').replace('_', ' ')
                array_tmp = list(filter(lambda x: category in (x.get('eventTopics')
                                                               if x.get('eventTopics') is not None else []), array))
                for item in array_tmp:
                    if item not in array_filtered:
                        array_filtered.append(item)
            array = array_filtered

        if mode == 'dict':
            return array
        elif mode == 'dotdict':
            return [DotDict(x) for x in array]
        elif mode == 'json':
            return json.dumps(array, indent=4, sort_keys=True, default=str)
        return self.events

    @security.public
    def import_events_from_url(self, url=None,
                               schema_output=None, schema_input=None, response_dict_key='events'):
        assert url is not None, 'url is required'
        assert schema_output is not None, 'schema_output is required'
        assert schema_input is not None, 'schema_input is required'

        response = requests.get(url=url)
        if response.status_code == 200:
            agenda = response.json()
        else:
            raise ImportError(url)
        if isinstance(agenda, dict) and response_dict_key in agenda.keys():
            agenda = agenda[response_dict_key]  # response_dict_key='events' for AgendaLibrary
        if isinstance(agenda, list):
            for item in agenda:
                event = schema_input.mapping(DotDict(item),
                                             self.locale)
                if event is not None:
                    self.events.append(schema_output.model_validate(event))
        return None

    @security.public
    def import_events_from_outlook(self, account=None,
                                   schema_output=None, schema_input=None):
        assert account is not None, 'account is required'
        assert schema_output is not None, 'schema_output is required'
        assert schema_input is not None, 'schema_input is required'

        outlook = OutlookConnector(account=account)
        calendar = json.loads(asyncio.run(outlook.get_calendar_events(start_date=self.start_date,
                                                                      end_date=self.end_date)))
        if isinstance(calendar, list):
            for item in calendar:
                attachments = None
                if item.get('hasAttachments'):
                    attachments = outlook.get_event_attachments(event_id=item.get('id'))
                event = schema_input.mapping(DotDict(item),
                                             attachments,
                                             self.locale)
                if event is not None:
                    self.events.append(schema_output.model_validate(event))
        return None
    
    @security.public
    def import_events_from_zms(self, context=None, lang=None, node=None, meta_id=None,
                               schema_output=None, schema_input=None):
        assert context is not None, 'context is required'
        assert lang is not None, 'lang is required'
        assert node is not None, 'node is required'
        assert meta_id is not None, 'meta_id is required'
        assert schema_output is not None, 'schema_output is required'
        assert schema_input is not None, 'schema_input is required'

        if (meta_id == 'ZMSAgendaRecordset'
            and hasattr(context, 'agenda_recordset')
            and context.agenda_recordset.isMetaType('ZMSAgendaRecordset')):
            items = context.agenda_recordset.attr('records')
        else:
            obj = context.getLinkObj(node)
            items = context.zcatalog_index({'meta_id': meta_id, 'path': obj.getPath()}) if obj is not None else None
        if isinstance(items, list) or isinstance(items, LazyMap):
            for item in items:
                try:
                    event = schema_input.mapping(DotDict(item) if meta_id == 'ZMSAgendaRecordset' else item.getObject(),
                                                 context, lang, self.locale)
                    if event is not None:
                        self.events.append(schema_output.model_validate(event))
                except Exception as e:
                    if isinstance(item, dict):
                        LOGGER.error(f'Error importing event: {e}')
                    else:
                        LOGGER.error(f'Error importing event: {item.get_uid} {item.getPath()} {e}')
        return None

    @security.public
    def import_events_from_csv(self):
        # TODO: Get events from a CSV file (e.g. Excel)
        raise NotImplementedError

    @staticmethod
    @security.public
    def get_calendar_ics(events=None):
        assert isinstance(events, list), 'events are required as list'

        calendar_ics = Calendar()
        for event in events:
            event_ics = Event()

            begin = local_timezone(event.get('eventStartDateTime'))
            end = local_timezone(event.get('eventEndDateTime'))

            event_ics.name = event.get('eventTitle')
            event_ics.begin = begin
            event_ics.end = end if begin <= end else begin
            event_ics.location = event.get('eventLocation')
            event_ics.description = event.get('eventInfos')
            event_ics.categories = event.get('eventTopics')
            event_ics.url = event.get('eventUrl')

            calendar_ics.events.add(event_ics)
        return calendar_ics.serialize()


# Apply security assertions by ClassSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#a-class-security-example
InitializeClass(AgendaBridge)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
