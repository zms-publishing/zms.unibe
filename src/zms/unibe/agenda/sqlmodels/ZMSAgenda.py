from datetime import datetime
from sqlmodel import Field, Column, DateTime, Date, String
from sqlalchemy.dialects import postgresql
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_data, parse_datetime, local_timezone


class ZMSAgenda(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    attr_dc_type: str | None
    path: str
    level: int
    hide_past_events: bool
    categories: list = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    categories_include_only: list = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    categories_filter_out: list = Field(default=None, sa_column=Column(postgresql.ARRAY(String())))
    include_filemaker: bool
    include_library: bool
    include_itstatusmessages: bool
    include_outlook: bool
    outlook_upn: str | None
    limit_time_range: bool
    begin_date: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))  # TODO: Date() stores 2026-01-30 instead of 2026-01-30 23:00:00.000000 +00:00 UTC = 31.01.2026 00:00 CET
    end_date: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))  # TODO: Date() stores 2025-09-29 instead of 2025-09-29 22:00:00.000000 +00:00 UTC = 30.09.2025 00:00 CET
    cached_data: str | None
    lastupdate: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

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
            'begin_date':               local_timezone(parse_datetime(obj.attr('begin_date')), tz='UTC'),
            'end_date':                 local_timezone(parse_datetime(obj.attr('end_date')), tz='UTC'),  # TODO: days_delta=1 to include end_date (="bis und mit") here as in OutlookConnector.get_calendar_events...?!
            'cached_data':              get_data(obj, '_datafilecached', json_as_py=False)[0],
            'lastupdate':               parse_datetime(obj.attr('_datalastupdated')),
        }
        return cls.model_validate(mapping)
