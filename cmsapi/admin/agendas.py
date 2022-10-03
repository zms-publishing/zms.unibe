import json
import requests
from datetime import datetime

from ..helpers import local_timezone
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN


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
        AgendaPortal.__table__.drop(sqlengine)
        AgendaPortal.__table__.create(sqlengine)
        for item in agenda_portal:
            item['json_datum_zeit_start'] = local_timezone(datetime.fromisoformat(item['json_datum_zeit_start']))
            item['json_datum_zeit_end'] = local_timezone(datetime.fromisoformat(item['json_datum_zeit_end']))
            session.add(AgendaPortal.parse_obj(item))
        session.commit()

    if agenda_library_de is not None:
        AgendaLibraryDE.__table__.drop(sqlengine)
        AgendaLibraryDE.__table__.create(sqlengine)
        for item in agenda_library_de:
            item['startsAt'] = local_timezone(datetime.fromisoformat(item['startsAt']))
            item['endsAt'] = local_timezone(datetime.fromisoformat(item['endsAt']))
            session.add(AgendaLibraryDE.parse_obj(item))
        session.commit()

    if agenda_library_en is not None:
        AgendaLibraryEN.__table__.drop(sqlengine)
        AgendaLibraryEN.__table__.create(sqlengine)
        for item in agenda_library_en:
            item['startsAt'] = local_timezone(datetime.fromisoformat(item['startsAt']))
            item['endsAt'] = local_timezone(datetime.fromisoformat(item['endsAt']))
            session.add(AgendaLibraryEN.parse_obj(item))
        session.commit()
