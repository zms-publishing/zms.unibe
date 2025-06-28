import traceback
from devtools import debug

from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.foundation.sqlmodels.ZMSSite import ZMSSite

from .attributes import get_attr_value


def map_obj_attributes(zmsindex_result, model, count_objs, verbose=False):

    rtn = []
    attrs = {}

    for i, x in enumerate(zmsindex_result):  # TODO: optimize retrieval for 1000+ objects
        try:
            obj = x.getObject()
            for sql_attr, zms_attr in {**ZMSBase.get_attr_mappings(), **model.get_attr_mappings()}.items():
                if (isinstance(count_objs, dict)
                        and sql_attr == 'count_objs'
                        and model == ZMSSite):
                    attrs[sql_attr] = count_objs[x]
                else:
                    attrs[sql_attr] = get_attr_value(sql_attr, zms_attr, obj, model)
        except Exception as e:
            if verbose:
                debug(x.get_uid, x.getPath(), x.id, x.meta_id)
                traceback.print_exc()
            continue
        rtn.append(
            model(**attrs))
    return rtn
