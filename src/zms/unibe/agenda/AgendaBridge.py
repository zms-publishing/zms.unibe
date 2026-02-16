# AgendaBridge aggregates events from different data sources
# see also sqlmodels/__main__.py to store in PostgreSQL for unibe.app

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
PREFIX = 'ZMSAgenda.Category.'


class AgendaBridge(ObjectManager):
    security = ClassSecurityInfo()  # control access to class methods in RestrictedPython
    
    def __init__(self, locale, accounts='', begin_date=None, end_date=None):
        self.events = []
        self.locale = locale
        self.accounts = (accounts.replace(';', ' ').replace(',', ' ')).split()
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
    def get_categories(self, translations=False):
        # WORKAROUND for FindCategoriesAccessDenied via MS Graph API
        #
        # With delegated permission MailboxSettings.Read* you cannot read outlook categories of other users.
        # The only way to read outlook categories is with application permission MailboxSettings.ReadWrite.
        #
        # With this application permission, you can limit the scope to a subset of mailboxes.
        # https://stackoverflow.com/questions/77825238/get-create-categories-for-any-user-in-outlook-calendar-with-graphapi
        url = os.getenv('AGENDA_CATEGORIES_URL', 'http://localhost:8081/unibe/agenda-categories.json')
        categories = []

        response = requests.get(url)
        if response.status_code == 200:
            agenda_categories = response.json()
        else:
            agenda_categories = {}
        
        if translations:
            categories = {}
            for category in agenda_categories.keys():
                if category.startswith('ZMSAgenda.Category.'):
                    categories[category] = agenda_categories[category]
            return categories
            
        for account in self.accounts:
            if account in agenda_categories.keys():
                categories.extend(agenda_categories[account])
        return list(set(categories))
            
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
    def import_events_from_outlook(self, schema_output=None, schema_input=None):
        assert schema_output is not None, 'schema_output is required'
        assert schema_input is not None, 'schema_input is required'

        for account in self.accounts:
            outlook = OutlookConnector(upn=account)
            calendar = json.loads(outlook.get_calendar_events(begin_date=self.begin_date, end_date=self.end_date))
            if isinstance(calendar, list):
                for item in calendar:
                    attachments = None
                    if item.get('hasAttachments'):
                        attachments = []
                        for attachment in outlook.get_event_attachments(event_id=item.get('id')):
                            attachments.append(schema_input.mapping_attachment(attachment))
                    event = schema_input.mapping(DotDict(item),
                                                 attachments,
                                                 account,
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
    def include_only(events, given_categories):
        if isinstance(given_categories, list) and len(given_categories) > 0:
            events_included = []
            for event in events:
                categories = event.get('eventCategories') if isinstance(event.get('eventCategories'), list) else []
                for category in categories:
                    category = f"{PREFIX}{category.replace(' ', '_')}"
                    if category in given_categories:
                        events_included.append(event)
                        break
            events = events_included
        return events

    @staticmethod
    def filter_out(events, given_categories):
        if isinstance(given_categories, list) and len(given_categories) > 0:
            events_filtered = events.copy()
            for event in events:
                categories = event.get('eventCategories') if isinstance(event.get('eventCategories'), list) else []
                for category in categories:
                    category = f"{PREFIX}{category.replace(' ', '_')}"
                    if category in given_categories:
                        events_filtered.remove(event)
                        break
            events = events_filtered
        return events


# Apply security assertions by ClassSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#a-class-security-example
InitializeClass(AgendaBridge)

# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())
