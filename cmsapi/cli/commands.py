import traceback
from sqlmodel import SQLModel, Session, select
from devtools import debug

from ..helpers import get_attr_value
from ..models.zmsdefaults import ZMSBase


def init_tables(models, *args):

    zmsindex, sqlengine = args

    with Session(sqlengine) as session:

        SQLModel.metadata.drop_all(sqlengine)
        SQLModel.metadata.create_all(sqlengine)

        for model in models:
            query = zmsindex({'meta_id': model.get_zms_metaid()})
            for obj in _iterate_over_content_objects(query, model):
                session.add(obj)
            session.commit()


def update_tables(models, *args):

    zmsindex, sqlengine = args

    for model in models:
        with Session(sqlengine) as session:
            query = zmsindex({'meta_id': model.get_zms_metaid()})
            for obj in _iterate_over_content_objects(query, model):
                statement = select(model).where(model.uuid == obj.uuid)
                results = session.exec(statement)
                row = results.first()
                if row is not None:
                    session.delete(row)
                session.add(obj)
            session.commit()


def _iterate_over_content_objects(query, model):

    rtn = []
    attrs = {}

    for i, x in enumerate(query):
        try:
            for sql_attr, zms_attr in {**model.get_attr_mappings(), **ZMSBase.get_attr_mappings()}.items():
                attrs[sql_attr] = get_attr_value(sql_attr, zms_attr, x.getObject(), model)
        except Exception as e:
            debug(x.get_uid)
            traceback.print_exc()
            continue
        rtn.append(
            model(**attrs))
    return rtn
