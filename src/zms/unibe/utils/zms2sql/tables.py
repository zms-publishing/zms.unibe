import time
import uuid
import collections
import traceback

from devtools import debug
from sqlmodel import SQLModel, Session, select, inspect

from zms.unibe.utils.db import connect_sqldb


def drop_create_sql_tables(model):
    
    sqlengine = connect_sqldb()
    
    # TODO: add SQL handling to drop and create all tables (or specific table)
    if _all:
        SQLModel.metadata.drop_all(sqlengine)
        SQLModel.metadata.create_all(sqlengine)
    else:
        for model in models:
            if inspect(sqlengine).has_table(model.__name__.lower()):
                model.__table__.drop(sqlengine)
                model.__table__.create(sqlengine)


def process_sql_updates(zmsindex_result, model, verbose=True):
    
    sqlengine = connect_sqldb(verbose=verbose)

    with Session(sqlengine) as session:

        t0 = time.time()
        print('--------------------------------------------------------------------------')
        print('Process', model)

        uuids_processed = []

        if not inspect(sqlengine).has_table(model.__name__.lower()):
            model.__table__.create(sqlengine)

        for item in zmsindex_result:
            try:
                if 'trashcan' in item.getPath():
                    continue
                obj = model.from_zms_obj(item.getObject())
                if obj is None:
                    continue
            except Exception as e:
                if verbose:
                    debug(item.get_uid, item.getPath(), item.id, item.meta_id)
                    traceback.print_exc()
                continue
            statement = select(model).where(model.uuid == obj.uuid)
            results = session.exec(statement)
            row = results.one_or_none()
            if row is None:
                # INSERT new obj
                try:
                    session.add(obj)
                    session.commit()
                # outside the intended container
                # to which the foreign key refers
                except:
                    session.rollback()
                    if verbose:
                        debug(obj)
                    continue
            else:
                # UPDATE existing row
                try:
                    row.sqlmodel_update(obj.model_dump())
                    session.add(row)
                    session.commit()
                    session.refresh(row)
                except:
                    session.rollback()
                    if verbose:
                        debug(row)
                    continue

            uuids_processed.append(uuid.UUID(f'urn:uuid:{obj.uuid}'))

        # DELETE CASCADE rows with obsolete uuids which are removed from ZODB
        # we define it for the foreign keys of models to set the PostgreSQL tables correctly
        # we omit the Relationship(back_populates="...", cascade_delete=True) mentioned in the docs
        # as we do not work the objects - we just want to auto-delete all referenced rows in SQL
        # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/
        statement = select(model.uuid)
        results = session.exec(statement)
        uuids_existing = results.all()
        if verbose:
            uuids_duplicate = [item for item, count in collections.Counter(uuids_processed).items() if count > 1]
            debug(uuids_duplicate)
        # remove duplicates by using set()
        uuids_obsolete = list(set(uuids_existing) - set(uuids_processed))
        if verbose:
            debug(uuids_obsolete)
        for uid in uuids_obsolete:
            statement = select(model).where(model.uuid == uid)
            results = session.exec(statement)
            row = results.one_or_none()
            if row is not None:
                session.delete(row)
                session.commit()

        statement = select(model)
        results = session.exec(statement)

        t1 = time.time()
        ts = t1 - t0
        print('--------------------------------------------------------------------------')
        print(model.__name__, f'({len(results.all()):,})', f'{ts:.3f} sec', f'= {ts / 60:.2f} min')
        print('==========================================================================')
