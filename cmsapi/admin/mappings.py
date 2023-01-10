import traceback
from devtools import debug

from ..helpers import get_attr_value
from ..models.zmsobjects import ZMSBase


def _iterate_content_objects(query, model):

    rtn = []
    attrs = {}

    for i, x in enumerate(query):  # TODO: optimize retrieval for 1000+ objects
        try:
            for sql_attr, zms_attr in {**ZMSBase.get_attr_mappings(), **model.get_attr_mappings()}.items():
                attrs[sql_attr] = get_attr_value(sql_attr, zms_attr, x.getObject(), model)
        except Exception as e:
            debug(x.get_uid, x.getPath(), x.id, x.meta_id)
            traceback.print_exc()
            continue
        rtn.append(
            model(**attrs))
    return rtn
