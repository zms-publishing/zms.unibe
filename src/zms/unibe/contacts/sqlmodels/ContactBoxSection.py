from uuid import UUID
from zms.unibe.foundation.sqlmodels.ZMSBase import ZMSBase
from zms.unibe.utils.helpers import get_attr, get_parent_node_uuid


class ContactBoxSection(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    intersection_title_de: str | None
    intersection_title_en: str | None
    intersection_title_fr: str | None
    interpara_title_de: str | None
    interpara_title_en: str | None
    interpara_title_fr: str | None
    contactbox_uuid: UUID

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'contactboxsection'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr                  # zms_attr
            'intersection_title_de':    get_attr(obj, 'intersection_title', 'ger'),
            'intersection_title_en':    get_attr(obj, 'intersection_title', 'eng'),
            'intersection_title_fr':    get_attr(obj, 'intersection_title', 'fra'),
            'interpara_title_de':       get_attr(obj, 'interpara_title', 'ger'),
            'interpara_title_en':       get_attr(obj, 'interpara_title', 'eng'),
            'interpara_title_fr':       get_attr(obj, 'interpara_title', 'fra'),
            'contactbox_uuid':          get_parent_node_uuid(obj),
        }
        return cls.model_validate(mapping)
