from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr


class ZMSTable(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    caption_de: str | None
    caption_en: str | None
    caption_fr: str | None
    descr_de: str | None
    descr_en: str | None
    descr_fr: str | None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSTable'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'caption_de':          get_attr(obj, 'caption', 'ger'),
            'caption_en':          get_attr(obj, 'caption', 'eng'),
            'caption_fr':          get_attr(obj, 'caption', 'fra'),
            'descr_de':            get_attr(obj, 'attr_dc_description', 'ger'),
            'descr_en':            get_attr(obj, 'attr_dc_description', 'eng'),
            'descr_fr':            get_attr(obj, 'attr_dc_description', 'fra'),
        }
        return cls.model_validate(mapping)
