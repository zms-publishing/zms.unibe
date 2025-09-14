from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr


class ContactBox(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    titlealt_de: str | None
    titlealt_en: str | None
    titlealt_fr: str | None
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    sections: int

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'contactbox'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'titlealt_de':      get_attr(obj, 'titlealt', 'ger'),
            'titlealt_en':      get_attr(obj, 'titlealt', 'eng'),
            'titlealt_fr':      get_attr(obj, 'titlealt', 'fra'),
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'sections':         obj.getObjChildren('sections'),  # TODO: check this - or use get_children_count(obj)?
        }
        return cls.model_validate(mapping)
