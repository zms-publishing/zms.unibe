from datetime import datetime

from ...foundation.sqlmodels.ZMSBase import ZMSBase


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

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'datatype':         'datatype',
            'dataremote':       'dataremote',
            'datawebservice':   'datawebservice',
            'dataurl_de':       'dataurl_ger',
            'dataurl_en':       'dataurl_eng',
            'dataurl_fr':       'dataurl_fra',
            'datafile_de':      'datafile_ger',
            'datafile_en':      'datafile_eng',
            'datafile_fr':      'datafile_fra',
            'cached_data_de':   'obj.getData(_datafilecached_ger)',
            'cached_data_en':   'obj.getData(_datafilecached_eng)',
            'cached_data_fr':   'obj.getData(_datafilecached_fra)',
            'upload_data_de':   'obj.getData(datafile_ger)',
            'upload_data_en':   'obj.getData(datafile_eng)',
            'upload_data_fr':   'obj.getData(datafile_fra)',
            'lastupdate':       '_datalastupdated',
        }
