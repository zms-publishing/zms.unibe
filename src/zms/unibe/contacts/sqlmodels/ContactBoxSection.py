from uuid import UUID

from ...foundation.sqlmodels.ZMSBase import ZMSBase


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
    def get_zms_metaid():
        return 'contactboxsection'

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'intersection_title_de':      'intersection_title_ger',
            'intersection_title_en':      'intersection_title_eng',
            'intersection_title_fr':      'intersection_title_fra',
            'interpara_title_de':         'interpara_title_ger',
            'interpara_title_en':         'interpara_title_eng',
            'interpara_title_fr':         'interpara_title_fra',
            'contactbox_uuid':            'obj.getParentNode()._uid',
        }
