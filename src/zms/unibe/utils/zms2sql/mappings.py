import traceback

from devtools import debug

from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from .attributes import get_attr_value


def map_obj_attributes(zmsindex_result, model, verbose=False):

    rtn = []
    attrs = {}

    for i, x in enumerate(zmsindex_result):  # TODO: optimize retrieval for 1000+ objects
        try:
            obj = x.getObject()
            for sql_attr, zms_attr in {**ZMSBase.get_attr_mappings(), **model.get_attr_mappings()}.items():
                attrs[sql_attr] = get_attr_value(sql_attr, zms_attr, obj, model)
        except Exception as e:
            if verbose:
                debug(x.get_uid, x.getPath(), x.id, x.meta_id)
                traceback.print_exc()
            continue
        rtn.append(
            model(**attrs))
    return rtn
