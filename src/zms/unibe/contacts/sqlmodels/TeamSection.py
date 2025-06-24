from uuid import UUID

from ...zmsfoundation.sqlmodels import ZMSBase


class TeamSection(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    team_uuid: UUID | None
    persons: int

    @staticmethod
    def get_zms_metaid():
        return 'teamsection'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'team_uuid':        'obj.getParentNode()._uid',
            'persons':          'obj.getObjChildren(person)',
        }
