import time
from sqlmodel import SQLModel, Session, select
from devtools import debug

from ..models.zmsobjects import ZMSSite
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from .agendas import _fetch_agenda_data
from .newsevents import _store_newsevents_data
from .zmsobjects import _iterate_content_objects


def init_tables(models, *args, _all=False):

    zmsindex, sqlengine = args

    for model in models:
        if model == ZMSSite:
            if _all:
                SQLModel.metadata.drop_all(sqlengine)
            SQLModel.metadata.create_all(sqlengine)
            update_tables((ZMSSite,), *args)
        else:
            model.__table__.drop(sqlengine)
            model.__table__.create(sqlengine)
            update_tables((model,), *args)


def update_tables(models, *args):

    zmsindex, sqlengine = args

    with Session(sqlengine) as session:

        for model in models:

            t0 = time.time()
            print('--------------------------------------------------------------------------')
            print('Process', model)

            if model in (AgendaPortal, AgendaLibraryDE, AgendaLibraryEN):
                _fetch_agenda_data(session, sqlengine)
                _store_newsevents_data(session, sqlengine)
            else:
                uuids_new = []
                query = zmsindex({'meta_id': model.get_zms_metaid()})  # TODO: optimize retrieval for 1000+ objects
                for obj in _iterate_content_objects(query, model):
                    statement = select(model).where(model.uuid == obj.uuid)
                    results = session.exec(statement)
                    row = results.first()
                    if row is not None:
                        session.delete(row)
                    session.add(obj)
                    uuids_new.append(obj.uuid)
                session.commit()

                # delete rows with obsolete uuids
                statement = select(model.uuid)
                results = session.exec(statement)
                uuids_all = results.all()
                uuids_del = list(set(uuids_all)-set(uuids_new))
                debug(uuids_del)
                for uuid in uuids_del:
                    statement = select(model).where(model.uuid == uuid)
                    results = session.exec(statement)
                    row = results.first()
                    if row is not None:
                        session.delete(row)
                session.commit()

            t1 = time.time()
            ts = t1 - t0
            print('--------------------------------------------------------------------------')
            print(model.__name__, ts / 60 > 1 and f': {ts / 60} min' or f': {ts} sec')
