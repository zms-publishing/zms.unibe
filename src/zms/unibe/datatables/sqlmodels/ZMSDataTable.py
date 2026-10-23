from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_data, get_url, local_timezone
from ...utils.types import OptionalDateTime


class ZMSDataTable(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    datatype: str
    dataremote: bool
    datawebservice: str | None = None
    dataurl_de: str | None = None
    dataurl_en: str | None = None
    dataurl_fr: str | None = None
    datafile_de: str | None = None
    datafile_en: str | None = None
    datafile_fr: str | None = None
    cached_data_de: str | None = None
    cached_data_en: str | None = None
    cached_data_fr: str | None = None
    upload_data_de: str | None = None
    upload_data_en: str | None = None
    upload_data_fr: str | None = None
    lastupdate: OptionalDateTime

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
            'lastupdate':       local_timezone(obj.attr('_datalastupdated')),
        }
        return cls.model_validate(mapping)
