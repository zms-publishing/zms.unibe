from uuid import UUID
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_children_count


class ContentPane(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    elements: int | None
    contenttabs_uuid: UUID

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'contentpane'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'elements':         get_children_count(obj),
            'contenttabs_uuid': obj.getParentNode()._uid,
        }
        return cls.model_validate(mapping)
