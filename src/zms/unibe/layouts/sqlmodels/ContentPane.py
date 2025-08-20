from uuid import UUID

from ...foundation.sqlmodels.ZMSBase import ZMSBase


class ContentPane(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    title_de: str | None
    title_en: str | None
    title_fr: str | None
    elements: int | None
    contenttabs_uuid: UUID

    @staticmethod
    def get_zms_metaid():
        return 'contentpane'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'elements':         'obj.getObjChildren(e)',
            'contenttabs_uuid': 'obj.getParentNode()._uid',
        }
