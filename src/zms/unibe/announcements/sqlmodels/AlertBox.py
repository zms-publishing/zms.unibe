from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.zms2sql.getters import get_attr


class AlertBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    type: str | None = None
    text_de: str | None = None
    text_en: str | None = None
    text_fr: str | None = None
    url_de: str | None = None
    url_en: str | None = None
    url_fr: str | None = None

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'alertbox'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'type':             obj.attr('alerttype'),
            'text_de':          get_attr(obj, 'text', 'ger'),
            'text_en':          get_attr(obj, 'text', 'eng'),
            'text_fr':          get_attr(obj, 'text', 'fra'),
            'url_de':           get_attr(obj, 'attr_url', 'ger'),
            'url_en':           get_attr(obj, 'attr_url', 'eng'),
            'url_fr':           get_attr(obj, 'attr_url', 'fra'),
        }
        return cls.model_validate(mapping)
