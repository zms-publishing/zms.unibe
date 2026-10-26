from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...helpers import local_timezone
from ...utils.types import OptionalDateTime, PostgreSQLArray
from ...utils.zms2sql.getters import get_attr, get_data


class ZMSAgenda(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    attr_dc_type: str | None = None
    hide_past_events: bool
    categories: PostgreSQLArray
    categories_include_only: PostgreSQLArray
    categories_filter_out: PostgreSQLArray
    include_filemaker: bool
    include_library: bool
    include_itstatusmessages: bool
    include_outlook: bool
    outlook_upn: str | None = None
    limit_time_range: bool
    begin_date: OptionalDateTime
    end_date: OptionalDateTime
    cached_data: str | None = None
    lastupdate: OptionalDateTime

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSAgenda'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr                  # zms_attr
            'attr_dc_type':             obj.attr('attr_dc_type'),
            'hide_past_events':         obj.attr('hide_past_events'),
            'categories':               get_attr(obj, '_categories'),
            'categories_include_only':  get_attr(obj, 'categories_include_only'),
            'categories_filter_out':    get_attr(obj, 'categories_filter_out'),
            'include_filemaker':        get_attr(obj, 'include_filemaker'),
            'include_library':          get_attr(obj, 'include_library'),
            'include_itstatusmessages': get_attr(obj, 'include_itstatusmessages'),
            'include_outlook':          get_attr(obj, 'include_outlook'),
            'outlook_upn':              get_attr(obj, 'outlook_upn'),
            'limit_time_range':         get_attr(obj, 'limit_time_range'),
            'begin_date':               local_timezone(
                local_timezone(obj.attr('begin_date')).date()),
            'end_date':                 local_timezone(
                local_timezone(obj.attr('end_date')).date()),
            'cached_data':              get_data(obj, '_datafilecached', json_as_py=False)[0],
            'lastupdate':               local_timezone(obj.attr('_datalastupdated')),
        }
        return cls.model_validate(mapping)
