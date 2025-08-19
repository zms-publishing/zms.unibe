import json
from datetime import datetime

import requests
from sqlmodel import inspect, Session

from zms.unibe.utils.db import connect_sqldb
from zms.unibe.utils.helpers import local_timezone
from .AgendaFilemaker import AgendaFilemaker
from .AgendaLibraryDE import AgendaLibraryDE
from .AgendaLibraryEN import AgendaLibraryEN


def fetch_agendas():

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


if __name__ == "__main__":
    fetch_agendas()
    