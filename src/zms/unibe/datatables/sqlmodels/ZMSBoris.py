from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.helpers import get_attr, get_data, get_url, local_timezone
from ...utils.types import OptionalDateTime


class ZMSBoris(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    dataurl: str | None = None
    descr_de: str | None = None
    descr_en: str | None = None
    descr_fr: str | None = None
    boris_data: str | None  # = Field(sa_column=Column(JSONB), default_factory=dict)
    lastupdate: OptionalDateTime

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSBoris'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'dataurl':          get_url(obj, 'dataurl'),
            'descr_de':         get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':         get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':         get_attr(obj, 'attr_dc_description', 'fra'),
            'boris_data':       get_data(obj, '_datafilecached', json_as_py=False)[0],
            'lastupdate':       local_timezone(obj.attr('_datalastupdated')),
        }
        return cls.model_validate(mapping)
