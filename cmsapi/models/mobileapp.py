from uuid import UUID

from .zmsobjects import ZMSBase


class MobileApp(ZMSBase, table=True):
    __table_args__ = {'extend_existing': True}
    path: str
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
            'path':             'obj.getPath()',
            'meta_id':          'obj.meta_id',
            'title_de':         'title',
            'title_en':         'title',
            'title_fr':         'title',
            'text_de':          'text',
            'text_en':          'text',
            'text_fr':          'text',
            'keywords_de':      'attr_dc_description',
            'keywords_en':      'attr_dc_description',
            'keywords_fr':      'attr_dc_description',
            'href_de':          'attr_ref',
            'href_en':          'attr_ref',
            'href_fr':          'attr_ref',
            'url_de':           'file',
            'url_en':           'file',
            'url_fr':           'file',
            'parent_uuid':      'obj.getParentNode()._uid',
            'parent_title_de':  'obj.getParentNode().attr("title")',
            'parent_title_en':  'obj.getParentNode().attr("title")',
            'parent_title_fr':  'obj.getParentNode().attr("title")',
        }
