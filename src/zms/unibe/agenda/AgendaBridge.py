# AgendaBridge aggregates events from different data sources
# see also sqlmodels/__main__.py to store in PostgreSQL for unibe.app

import asyncio
import requests
import json
import logging
import os

from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager  # inherit from to use ClassSecurityInfo
from ZTUtils.Lazy import LazyMap
from operator import attrgetter

from ..utils.helpers import DotDict, local_timezone
from .OutlookConnector import OutlookConnector


print('Addon: zms.unibe.agenda.AgendaBridge')
security = ModuleSecurityInfo('zms.unibe.agenda.AgendaBridge')  # allow module import in RestrictedPython

LOGGER = logging.getLogger('ZMSAgenda')


class AgendaBridge(ObjectManager):
    security = ClassSecurityInfo()  # control access to class methods in RestrictedPython
    
    def __init__(self, locale, begin_date=None, end_date=None):
        self.events = []
        self.locale = locale
        self.begin_date = local_timezone(begin_date)
        self.end_date = local_timezone(end_date)

    @security.public    
    def get_events(self, mode=None):
        events = [x.model_dump() for x in sorted(
            self.events,
            key=attrgetter('eventBeginDateTime', 'eventEndDateTime')
        )]

        if mode == 'dict':
            return events
        elif mode == 'dotdict':
            return [DotDict(x) for x in events]
        elif mode == 'json':
            return json.dumps(events, indent=4, sort_keys=True, default=str)
        return self.events

    @security.public    
    def get_categories(self, upn):
        # WORKAROUND for FindCategoriesAccessDenied via MS Graph API
        # see zms-addons: zms.unibe.agenda.OutlookConnector.py.debug_calendar_categories
        # see zms-fastapi: cmsapi.zmscontent.routers.agenda.get_agenda_categories_by_upn
        url = os.getenv('ZMS_FASTAPI_URL', 'http://localhost:5003')
        endpoint = f'/v3/zms/content/agenda/{upn}/categories'
        
        if upn.endswith('@campus.unibe.ch'):
            response = requests.get(f'{url}{endpoint}')
            if response.status_code == 200:
                return response.json()
        
        return []
            
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
        calendar = json.loads(asyncio.run(outlook.get_calendar_events(begin_date=self.begin_date,
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


# Apply security assertions by ClassSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#a-class-security-example
InitializeClass(AgendaBridge)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
