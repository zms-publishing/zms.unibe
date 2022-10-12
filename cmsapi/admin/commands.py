import time
from sqlmodel import SQLModel, Session, select, inspect
from devtools import debug

from ..models.zmsobjects import ZMSSite
from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.mobileapp import MobileApp
from ..models.newsbox import Newsbox
from .agendas import _fetch_agenda_data, _fetch_status_messages
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
            if inspect(sqlengine).has_table(model.__table__):
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
                if not inspect(sqlengine).has_table(model.__table__):
                    model.__table__.create(sqlengine)
                if model == MobileApp:
                    query = zmsindex({'path': '/unibe/uniapp/content/'})
                elif model == Newsbox:
                    query = zmsindex({'path': '/unibe/portal/unibiblio/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_theologie/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_rechtwis/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_wiso/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_medizin/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_vetmedizin/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_historisch/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_humanwis/content', 'meta_id': 'newsbox'})
                    query += zmsindex({'path': '/unibe/portal/fak_naturwis/content', 'meta_id': 'newsbox'})
                else:
                    query = zmsindex({'meta_id': model.get_zms_metaid()})  # TODO: optimize retrieval for 1000+ objects

                uuids_new = []

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
