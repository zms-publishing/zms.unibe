from uuid import UUID

from .zmsobjects import ZMSBase


class ServiceLink(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    meta_id: str
    title_de: str
    title_en: str
    title_fr: str
    text_de: str | None
    text_en: str | None
    text_fr: str | None
    keywords_de: str | None
    keywords_en: str | None
    keywords_fr: str | None
    href_de: str | None
    href_en: str | None
    href_fr: str | None
    url_de: str | None
    url_en: str | None
    url_fr: str | None
    parent_uuid: UUID
    parent_title_de: str
    parent_title_en: str
    parent_title_fr: str

    @staticmethod
    def get_attr_mappings():
        return {
            # sql_attr          # zms_attr
            'meta_id':          'obj.meta_id',
            'title_de':         'title_ger',
            'title_en':         'title_eng',
            'title_fr':         'title_fra',
            'text_de':          'text_ger',
            'text_en':          'text_eng',
            'text_fr':          'text_fra',
            'keywords_de':      'attr_dc_description_ger',
            'keywords_en':      'attr_dc_description_eng',
            'keywords_fr':      'attr_dc_description_fra',
            'href_de':          'attr_ref_ger',
            'href_en':          'attr_ref_eng',
            'href_fr':          'attr_ref_fra',
            'url_de':           'file_ger',
            'url_en':           'file_eng',
            'url_fr':           'file_fra',
            'parent_uuid':      'obj.getParentNode()._uid',
            'parent_title_de':  'obj.getParentNode().title_ger',
            'parent_title_en':  'obj.getParentNode().title_eng',
            'parent_title_fr':  'obj.getParentNode().title_fra',
        }
