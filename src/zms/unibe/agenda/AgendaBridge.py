# Aggregate events from different data sources
# see implementation for unibe.app
# https://github.com/idasm-unibe-ch/zms-fastapi/blob/main/cmsapi/admin/agendas.py

import asyncio
import requests
import json

from .OutlookConnector import OutlookConnector
from .schemas import (
    AgendaFilemaker, 
    AgendaLibrary,
    AgendaOutlook,
    ZMSObjects,
    ZMSAgenda,
)
from ..utils.helpers import DotDict
from AccessControl import ModuleSecurityInfo, ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.ObjectManager import ObjectManager  # inherit from to use ClassSecurityInfo
from operator import attrgetter


print('Addon: zms.unibe.agenda.AgendaBridge')
security = ModuleSecurityInfo('zms.unibe.agenda.AgendaBridge')  # allow module import in RestrictedPython


class AgendaBridge(ObjectManager):
    security = ClassSecurityInfo()  # control access to class methods in RestrictedPython
    
    def __init__(self, locale):
        self.events = []
        self.locale = locale
    
    @security.public    
    def get_events(self, mode=None):
        array = [x.model_dump() for x in sorted(
            self.events,
            key=attrgetter('eventStartDateTime', 'eventEndDateTime')
        )]
        if mode == 'dict':
            return array
        elif mode == 'dotdict':
            return [DotDict(x) for x in array]
        elif mode == 'json':
            return json.dumps(array, indent=4, sort_keys=True, default=str)
        return self.events

    @security.public
    def import_events_from_filemaker(self):
        url = 'https://agenda.unibe.ch/agenda.json'
        response = requests.get(url=url)
        if response.status_code == 200:
            agenda_filemaker = response.json()
        else:
            raise ImportError(url)
        if agenda_filemaker is not None:
            for item in agenda_filemaker:
                event = AgendaFilemaker.mapping(DotDict(item), self.locale)
                if event is not None:
                    self.events.append(ZMSAgenda.Event.model_validate(event))
        return None

    @security.public
    def import_events_from_library(self):
        url = f'https://agenda.ub.unibe.ch/{self.locale}/api/event?limit=100'
        response = requests.get(url=url)
        if response.status_code == 200:
            agenda_library = response.json()
        else:
            raise ImportError(url)
        if agenda_library is not None:
            for item in agenda_library['events']:
                event = AgendaLibrary.mapping(item)
                if event is not None:
                    self.events.append(ZMSAgenda.Event.model_validate(event))
        return None

    @security.public
    def import_events_from_outlook(self, account=None):
        if account is not None:
            outlook = OutlookConnector(account=account)
            agenda_outlook = json.loads(asyncio.run(outlook.get_calendar_events()))
            if agenda_outlook is not None:
                for item in agenda_outlook:
                    event = AgendaOutlook.mapping(item)
                    if event is not None:
                        self.events.append(ZMSAgenda.Event.model_validate(event))
        return None
    
    @security.public
    def import_events_from_zms(self, zmsindex=None, path=None, lang=None, types=None):
        if (zmsindex is not None and 
                path is not None and 
                lang is not None):
            if isinstance(types, str):
                types = [types]
            if types is None or len(types) == 0:
                return None
            for meta_id in types:
                agenda_objects = zmsindex({'meta_id': meta_id, 'path': path})
                if agenda_objects is not None:
                    for item in agenda_objects:
                        event = ZMSObjects.mapping(item=item.getObject(),
                                                   meta_id=meta_id,
                                                   lang=lang)
                        if event is not None:
                            self.events.append(ZMSAgenda.Event.model_validate(event))
        return None

    @security.public
    def import_events_from_recordset(self, obj=None, lang=None):
        if (hasattr(obj, 'agenda_recordset')
                and obj.agenda_recordset.isMetaType('ZMSAgendaRecordset')):
            for item in obj.agenda_recordset.attr('records'):
                event = ZMSObjects.mapping(item, 
                                           meta_id='ZMSAgendaRecordset', 
                                           obj=obj, 
                                           lang=lang)
                if event is not None:
                    self.events.append(ZMSAgenda.Event.model_validate(event))
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
