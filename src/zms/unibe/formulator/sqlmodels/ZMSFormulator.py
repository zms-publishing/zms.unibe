from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_children_count, get_json_schema


class ZMSFormulator(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str
    title_en: str
    title_fr: str
    items: int | None
    json_schema: str

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'ZMSFormulator'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'items':            get_children_count(obj, 'ZMSFormulatorItem'),
            'json_schema':      get_json_schema(obj),
        }
        return cls.model_validate(mapping)
