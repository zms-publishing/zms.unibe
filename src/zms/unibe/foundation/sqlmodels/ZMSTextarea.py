from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr


class ZMSTextarea(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    format: str
    layout: str | None

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
