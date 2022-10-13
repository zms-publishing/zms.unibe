import json
import time
import requests
from datetime import datetime
from devtools import debug
from sqlmodel import inspect

from ..helpers import local_timezone
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.newsevents import StatusMessage


def _fetch_agenda_data(session, sqlengine):

    response = requests.get(url='https://agenda.unibe.ch/agenda.json')
    if response.status_code == 200:
        agenda_portal = response.json()
    else:
        raise ImportError

    response = requests.get(url='https://agenda.ub.unibe.ch/de/api/event?limit=100')
    if response.status_code == 200:
        agenda_library_de = json.loads(response.text.replace('event-type', 'eventType'))['events']  # TODO: eventType
    else:
        raise ImportError

    response = requests.get(url='https://agenda.ub.unibe.ch/en/api/event?limit=100')
    if response.status_code == 200:
        agenda_library_en = json.loads(response.text.replace('event-type', 'eventType'))['events']  # TODO: eventType
    else:
        raise ImportError

    if agenda_portal is not None:
        if inspect(sqlengine).has_table(AgendaPortal.__table__):
            AgendaPortal.__table__.drop(sqlengine)
        AgendaPortal.__table__.create(sqlengine)
        for item in agenda_portal:
            item['json_datum_zeit_start'] = local_timezone(datetime.fromisoformat(item['json_datum_zeit_start']))
            item['json_datum_zeit_end'] = local_timezone(datetime.fromisoformat(item['json_datum_zeit_end']))
            session.add(AgendaPortal.parse_obj(item))
        session.commit()

    if agenda_library_de is not None:
        if inspect(sqlengine).has_table(AgendaLibraryDE.__table__):
            AgendaLibraryDE.__table__.drop(sqlengine)
        AgendaLibraryDE.__table__.create(sqlengine)
        for item in agenda_library_de:
            item['startsAt'] = local_timezone(datetime.fromisoformat(item['startsAt']))
            item['endsAt'] = local_timezone(datetime.fromisoformat(item['endsAt']))
            session.add(AgendaLibraryDE.parse_obj(item))
        session.commit()

    if agenda_library_en is not None:
        if inspect(sqlengine).has_table(AgendaLibraryEN.__table__):
            AgendaLibraryEN.__table__.drop(sqlengine)
        AgendaLibraryEN.__table__.create(sqlengine)
        for item in agenda_library_en:
            item['startsAt'] = local_timezone(datetime.fromisoformat(item['startsAt']))
            item['endsAt'] = local_timezone(datetime.fromisoformat(item['endsAt']))
            session.add(AgendaLibraryEN.parse_obj(item))
        session.commit()


def _fetch_status_messages(session, sqlengine):

    data_host = 'https://www.unibe.ch'
    data_path = '/unibe/portal/content/e809/e946/e8896/e1217283/e1222429'  # Portal > IT Services > Status
    data_file = f'{data_host}{data_path}/ZMSDataTable_data_?{str(time.time())}'  # add time to bypass cache
    data_href = requests.get(url=data_file).text

    debug(data_host + data_href)
    response = requests.get(url=data_host + data_href)
    if response.status_code != 200 or \
            not data_href.startswith(data_path):
        raise ImportError

    status_messages = response.json()
    if status_messages is not None:
        if inspect(sqlengine).has_table(StatusMessage.__table__):
            StatusMessage.__table__.drop(sqlengine)
        StatusMessage.__table__.create(sqlengine)
        for item in status_messages:
            item['begin'] = local_timezone(datetime.fromisoformat(item['begin']))
            item['end'] = item['end'] is not None and local_timezone(datetime.fromisoformat(item['end']))
            session.add(StatusMessage.parse_obj(item))
        session.commit()
