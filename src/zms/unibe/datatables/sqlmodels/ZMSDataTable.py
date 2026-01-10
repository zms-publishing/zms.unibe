from datetime import datetime
from sqlmodel import Field, Column, DateTime
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_url, get_data, parse_datetime


class ZMSDataTable(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    datatype: str
    dataremote: bool
    datawebservice: str | None
    dataurl_de: str | None
    dataurl_en: str | None
    dataurl_fr: str | None
    datafile_de: str | None
    datafile_en: str | None
    datafile_fr: str | None
    cached_data_de: str | None
    cached_data_en: str | None
    cached_data_fr: str | None
    upload_data_de: str | None
    upload_data_en: str | None
    upload_data_fr: str | None
    lastupdate: datetime | None = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSDataTable'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'datatype':         obj.attr('datatype'),
            'dataremote':       obj.attr('dataremote'),
            'datawebservice':   obj.attr('datawebservice'),
            'dataurl_de':       get_url(obj, 'dataurl', 'ger'),
            'dataurl_en':       get_url(obj, 'dataurl', 'eng'),
            'dataurl_fr':       get_url(obj, 'dataurl', 'fra'),
            'datafile_de':      get_url(obj, 'datafile', 'ger'),
            'datafile_en':      get_url(obj, 'datafile', 'eng'),
            'datafile_fr':      get_url(obj, 'datafile', 'fra'),
            'cached_data_de':   get_data(obj, '_datafilecached', 'ger', json_as_py=False)[0],
            'cached_data_en':   get_data(obj, '_datafilecached', 'eng', json_as_py=False)[0],
            'cached_data_fr':   get_data(obj, '_datafilecached', 'fra', json_as_py=False)[0],
            'upload_data_de':   get_data(obj, 'datafile', 'ger', json_as_py=False)[0],
            'upload_data_en':   get_data(obj, 'datafile', 'eng', json_as_py=False)[0],
            'upload_data_fr':   get_data(obj, 'datafile', 'fra', json_as_py=False)[0],
            'lastupdate':       parse_datetime(obj.attr('_datalastupdated')),
        }
        return cls.model_validate(mapping)
