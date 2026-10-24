from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.zms2sql.getters import get_attr


class ZMSTextarea(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    text_de: str | None = None
    text_en: str | None = None
    text_fr: str | None = None
    format: str
    layout: str | None = None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSTextarea'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'text_de':          get_attr(obj, 'text', 'ger'),
            'text_en':          get_attr(obj, 'text', 'eng'),
            'text_fr':          get_attr(obj, 'text', 'fra'),
            'format':           obj.attr('format'),
            'layout':           obj.attr('attr_dc_type_layout'),
        }
        return cls.model_validate(mapping)
