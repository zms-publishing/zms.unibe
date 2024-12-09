import traceback
from devtools import debug

from ..helpers import get_attr_value
from ..models.zmsobjects import ZMSBase, ZMSSite


def _iterate_content_objects(query, model, count_objs):

    rtn = []
    attrs = {}

    for i, x in enumerate(query):  # TODO: optimize retrieval for 1000+ objects
        try:
            obj = x.getObject()
            for sql_attr, zms_attr in {**ZMSBase.get_attr_mappings(), **model.get_attr_mappings()}.items():
                if sql_attr == 'count_objs' and model == ZMSSite:
                    attrs[sql_attr] = count_objs[x]
                else:
                    attrs[sql_attr] = get_attr_value(sql_attr, zms_attr, obj, model)
        except Exception as e:
            debug(x.get_uid, x.getPath(), x.id, x.meta_id)
            traceback.print_exc()
            continue
        rtn.append(
            model(**attrs))
    return rtn
