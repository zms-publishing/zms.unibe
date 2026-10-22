import json
import time
from datetime import datetime

import requests
from devtools import debug
from sqlmodel import Session, inspect

from .AgendaFilemaker import AgendaFilemaker
from .AgendaLibraryDE import AgendaLibraryDE
from .AgendaLibraryEN import AgendaLibraryEN
from .StatusMessages import StatusMessage
from .ZMSAgenda import ZMSAgenda
from ...utils.db import connect_sqldb
from ...utils.helpers import local_timezone
from ...utils.zms2sql import zms2sql


def update_agendas(zms_context):
    zms2sql([ZMSAgenda], zms_context)


def fetch_agendas():
    print("fetch_agendas")

    try:
        response = requests.get(url='https://agenda.unibe.ch/agenda.json', timeout=5)
        if response.status_code == 200:
            agenda_portal = response.json()
    except Exception as e:
        print(f"Error fetching agendas: {e}")
        agenda_portal = None
    
    try:
        response = requests.get(url='https://agenda.ub.unibe.ch/de/api/event?limit=100', timeout=5)
        if response.status_code == 200:
            agenda_library_de = response.json()['events']
    except Exception as e:
        print(f"Error fetching agendas: {e}")
        agenda_library_de = None
    
    try:
        response = requests.get(url='https://agenda.ub.unibe.ch/en/api/event?limit=100', timeout=5)
        if response.status_code == 200:
            agenda_library_en = response.json()['events']
    except Exception as e:
        print(f"Error fetching agendas: {e}")
        agenda_library_en = None

    sqlengine = connect_sqldb()
    session = Session(sqlengine)

    if agenda_portal is not None:
        if inspect(sqlengine).has_table(AgendaFilemaker.__name__.lower()):
            AgendaFilemaker.__table__.drop(sqlengine)
        AgendaFilemaker.__table__.create(sqlengine)
        for item in agenda_portal:
            item['id'] = None
            try:
                item['json_datum_zeit_start'] = local_timezone(datetime.fromisoformat(item['json_datum_zeit_start']))
                item['json_datum_zeit_end'] = local_timezone(datetime.fromisoformat(item['json_datum_zeit_end']))
            except (ValueError, TypeError):
                continue
            session.add(AgendaFilemaker.model_validate(item))
        session.commit()

    if agenda_library_de is not None:
        if inspect(sqlengine).has_table(AgendaLibraryDE.__name__.lower()):
            AgendaLibraryDE.__table__.drop(sqlengine)
        AgendaLibraryDE.__table__.create(sqlengine)
        for item in agenda_library_de:
            item['id'] = None
            item['startsAt'] = local_timezone(datetime.fromisoformat(item['startsAt']))
            item['endsAt'] = local_timezone(datetime.fromisoformat(item['endsAt']))
            session.add(AgendaLibraryDE.model_validate(item))
        session.commit()

    if agenda_library_en is not None:
        if inspect(sqlengine).has_table(AgendaLibraryEN.__name__.lower()):
            AgendaLibraryEN.__table__.drop(sqlengine)
        AgendaLibraryEN.__table__.create(sqlengine)
        for item in agenda_library_en:
            item['id'] = None
            item['startsAt'] = local_timezone(datetime.fromisoformat(item['startsAt']))
            item['endsAt'] = local_timezone(datetime.fromisoformat(item['endsAt']))
            session.add(AgendaLibraryEN.model_validate(item))
        session.commit()


def fetch_statusmessages():
    print("fetch_statusmessages")

    sqlengine = connect_sqldb()
    with Session(sqlengine) as session:
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
            if inspect(sqlengine).has_table(StatusMessage.__name__.lower()):
                StatusMessage.__table__.drop(sqlengine)
            StatusMessage.__table__.create(sqlengine)
            for item in status_messages:
                item['id'] = None
                item['begin'] = local_timezone(datetime.fromisoformat(item['begin']))
                item['end'] = item['end'] is not None and local_timezone(datetime.fromisoformat(item['end'])) or None
                session.add(StatusMessage.model_validate(item))
            session.commit()
