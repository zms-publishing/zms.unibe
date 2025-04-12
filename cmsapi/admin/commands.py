import time
from sqlmodel import SQLModel, Session, select, inspect
from devtools import debug
from pathlib import Path

from ..models.agendas import AgendaPortal, AgendaLibraryDE, AgendaLibraryEN
from ..models.newsevents import StatusMessage
from ..models.servicelinks import ServiceLink
from ..models.newsbox import NewsBox
from ..models.uniaktuell import UniaktuellArticle
from ..models.mediareleases import MediaRelease
from ..models.zmsobjects import ZMSSite
from .agendas import _fetch_agenda_data, _fetch_status_messages
from .newsevents import _store_newsevents_data
from .mappings import _iterate_content_objects


def init_tables(models, *args, _all=False):

    zmsindex, sqlengine = args

    if _all:
        SQLModel.metadata.drop_all(sqlengine)
        SQLModel.metadata.create_all(sqlengine)
    else:
        for model in models:
            if inspect(sqlengine).has_table(model.__name__.lower()):
                model.__table__.drop(sqlengine)
                model.__table__.create(sqlengine)
    
    for model in models:
        update_tables((model,), *args)


def update_tables(models, *args):

    zmsindex, sqlengine = args

    with Session(sqlengine) as session:

        for model in models:

            t0 = time.time()
            print('--------------------------------------------------------------------------')
            print('Process', model)

            count_objs = {}
            
            if model in (AgendaPortal, AgendaLibraryDE, AgendaLibraryEN):
                _fetch_agenda_data(session, sqlengine)
            elif model == StatusMessage:
                _fetch_status_messages(session, sqlengine)
            else:
                if not inspect(sqlengine).has_table(model.__name__.lower()):
                    model.__table__.create(sqlengine)
                if model == ServiceLink:
                    query = zmsindex({'path': '/unibe/uniapp/content/'})
                elif model == NewsBox:
                    query = zmsindex({'path': '/unibe/portal/unibiblio/content', 'meta_id': 'newsbox'})
                    for newscontainer in open(f'{Path( __file__ ).parent.absolute()}/newsbox_all_active_filtered.csv'):
                        query += zmsindex({'path': f'{newscontainer.strip()}', 'meta_id': 'newsbox'})
                elif model == UniaktuellArticle:
                    query = zmsindex({'path': '/unibe/portal/uni_aktuell/content/e1325567',  # 2023
                                      'meta_id': 'UniaktuellArticle'})
                    query += zmsindex({'path': '/unibe/portal/uni_aktuell/content/e1325606',  # 2022
                                       'meta_id': 'UniaktuellArticle'})
                    query += zmsindex({'path': '/unibe/portal/uni_aktuell/content/e1327025',  # 2021
                                       'meta_id': 'UniaktuellArticle'})
                elif model == MediaRelease:
                    query = zmsindex({'path': '/unibe/portal/content/e796/e803/e59463/e805/e1311044/e1311045',  # 2023
                                      'meta_id': 'media_news'})
                    query += zmsindex({'path': '/unibe/portal/content/e796/e803/e59463/e805/e1160710/e1162114',  # 2022
                                       'meta_id': 'media_news'})
                    query += zmsindex({'path': '/unibe/portal/content/e796/e803/e59463/e805/e1027714/e1029489',  # 2021
                                       'meta_id': 'media_news'})
                elif model == ZMSSite:
                    query = zmsindex({'meta_id': 'ZMS'})
                    for site in query:
                        count_objs[site] = len(zmsindex({'path': site.getPath()}))
                else:
                    query = zmsindex({'meta_id': model.get_zms_metaid()})  # TODO: optimize retrieval for 1000+ objects

                for obj in _iterate_content_objects(query, model, count_objs):
                    statement = select(model).where(model.uuid == obj.uuid)
                    results = session.exec(statement)
                    row = results.one_or_none()
                    if row is None:
                        # INSERT new obj
                        try:
                            session.add(obj)
                            session.commit()
                        except:
                            session.rollback()
                            debug(obj)  # outside the intended container to which the foreign key refers
                    else:
                        # UPDATE existing row
                        row.sqlmodel_update(obj.model_dump())
                        session.add(row)
                        session.commit()
                        session.refresh(row)

            statement = select(model)
            results = session.exec(statement)

            t1 = time.time()
            ts = t1 - t0
            print('--------------------------------------------------------------------------')
            print(model.__name__, f'({len(results.all()):,})', f'{ts:.3f} sec', f'= {ts/60:.2f} min')

        # refresh intermediate NewsEvents table consolidating data sources for queries
        _store_newsevents_data(session, sqlengine)
