from uuid import UUID

from ...foundation.sqlmodels.ZMSBase import ZMSBase
from ...utils.zms2sql.getters import get_attr, get_children_count, get_parent_node_uuid


class TeamSection(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None = None
    title_en: str | None = None
    title_fr: str | None = None
    team_uuid: UUID | None = None
    persons: int

    @staticmethod
    def get_zms_catalog_query():
        return {'meta_id': 'teamsection'}

    @classmethod
    def from_zms_obj(cls, obj):
        mapping = {
            **ZMSBase.get_attr_mappings(obj),
            # sql_attr          # zms_attr
            'title_de':         get_attr(obj, 'title', 'ger'),
            'title_en':         get_attr(obj, 'title', 'eng'),
            'title_fr':         get_attr(obj, 'title', 'fra'),
            'team_uuid':        get_parent_node_uuid(obj),
            'persons':          get_children_count(obj, 'person'),
        }
        return cls.model_validate(mapping)
