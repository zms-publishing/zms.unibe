import traceback
from sqlmodel import SQLModel, Session
from devtools import debug

from ..helpers import get_attr_value
from ..models.zmsdefaults import ZMSBase


def init_tables(models, *args):

    zmsindex, sqlengine = args
    rtn = []
    attrs = {}

    for model in models:
        try:
            model.__table__.drop(sqlengine)
        except:
            pass
        SQLModel.metadata.create_all(sqlengine)

        for i, x in enumerate(zmsindex({'meta_id': model.get_zms_metaid()})):
            try:
                for sql_attr, zms_attr in {**model.get_attr_mappings(), **ZMSBase.get_attr_mappings()}.items():
                    attrs[sql_attr] = get_attr_value(sql_attr, zms_attr, x.getObject(), model)
            except Exception as e:
                debug(x.get_uid)
                traceback.print_exc()
                continue
            rtn.append(
                model(**attrs))

        with Session(sqlengine) as session:
            for obj in rtn:
                session.add(obj)
            session.commit()
