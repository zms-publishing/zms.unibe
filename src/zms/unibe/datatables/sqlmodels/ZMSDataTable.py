from datetime import datetime
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_url


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
    lastupdate: datetime | None

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
            'cached_data_de':   'obj.getData(_datafilecached_ger)',  # TODO: retrieve _datafilecached in common helper function
            'cached_data_en':   'obj.getData(_datafilecached_eng)',  # TODO: retrieve _datafilecached in common helper function
            'cached_data_fr':   'obj.getData(_datafilecached_fra)',  # TODO: retrieve _datafilecached in common helper function
            'upload_data_de':   'obj.getData(datafile_ger)',  # TODO: retrieve _datafilecached in common helper function
            'upload_data_en':   'obj.getData(datafile_eng)',  # TODO: retrieve _datafilecached in common helper function
            'upload_data_fr':   'obj.getData(datafile_fra)',  # TODO: retrieve _datafilecached in common helper function
            'lastupdate':       obj.attr('_datalastupdated'),
        }
        return cls.model_validate(mapping)
